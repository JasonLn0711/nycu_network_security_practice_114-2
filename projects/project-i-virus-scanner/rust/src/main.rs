mod bloom;
mod patterns;
mod reporting;
mod scanner;
mod signatures;

use std::path::PathBuf;

use reporting::{write_json_report, write_markdown_report};
use scanner::scan_directory;
use signatures::load_signature_database;

const VERSION: &str = env!("CARGO_PKG_VERSION");

#[derive(Debug)]
struct ScanArgs {
    target: PathBuf,
    signatures: PathBuf,
    json_report: PathBuf,
    markdown_report: PathBuf,
}

fn main() {
    let exit_code = match run(std::env::args().skip(1).collect()) {
        Ok(code) => code,
        Err(message) => {
            eprintln!("error: {message}");
            2
        }
    };
    std::process::exit(exit_code);
}

fn run(args: Vec<String>) -> Result<i32, String> {
    match args.first().map(String::as_str) {
        Some("--version") | Some("-V") => {
            println!("sentinel-v2-rust {VERSION}");
            Ok(0)
        }
        Some("validate-signatures") => {
            let signatures = parse_value_arg(&args[1..], "--signatures")
                .map(PathBuf::from)
                .unwrap_or_else(default_signature_path);
            let database = load_signature_database(&signatures)?;
            println!(
                "signature database ok: schema={} signatures={} hash_matchers={} patterns={}",
                database.schema_version,
                database.signatures.len(),
                database.hash_matcher_count(),
                database.patterns.len()
            );
            Ok(0)
        }
        Some("scan") => {
            let scan_args = parse_scan_args(&args[1..])?;
            let database = load_signature_database(&scan_args.signatures)?;
            let report = scan_directory(&scan_args.target, &database)?;
            write_json_report(&report, &scan_args.json_report)?;
            write_markdown_report(&report, &scan_args.markdown_report)?;

            println!(
                "Sentinel v2 Rust scan complete: scanned={} infected={} suspicious={} clean={} errors={} json={} markdown={}",
                report.summary.files_scanned,
                report.summary.infected,
                report.summary.suspicious,
                report.summary.clean,
                report.summary.error,
                scan_args.json_report.display(),
                scan_args.markdown_report.display()
            );

            if report.summary.infected > 0 {
                Ok(1)
            } else {
                Ok(0)
            }
        }
        _ => {
            print_usage();
            Ok(2)
        }
    }
}

fn parse_scan_args(args: &[String]) -> Result<ScanArgs, String> {
    Ok(ScanArgs {
        target: parse_value_arg(args, "--target")
            .map(PathBuf::from)
            .unwrap_or_else(default_target_path),
        signatures: parse_value_arg(args, "--signatures")
            .map(PathBuf::from)
            .unwrap_or_else(default_signature_path),
        json_report: parse_value_arg(args, "--json")
            .map(PathBuf::from)
            .unwrap_or_else(|| PathBuf::from("../reports/demo-report-rust.json")),
        markdown_report: parse_value_arg(args, "--markdown")
            .map(PathBuf::from)
            .unwrap_or_else(|| PathBuf::from("../reports/demo-report-rust.md")),
    })
}

fn parse_value_arg(args: &[String], name: &str) -> Option<String> {
    let mut index = 0;
    while index < args.len() {
        if args[index] == name {
            return args.get(index + 1).cloned();
        }
        index += 1;
    }
    None
}

fn default_signature_path() -> PathBuf {
    first_existing(&[
        "signatures/malware-signatures.json",
        "../signatures/malware-signatures.json",
    ])
}

fn default_target_path() -> PathBuf {
    first_existing(&["demo/demo-tree", "../demo/demo-tree"])
}

fn first_existing(candidates: &[&str]) -> PathBuf {
    candidates
        .iter()
        .map(PathBuf::from)
        .find(|path| path.exists())
        .unwrap_or_else(|| PathBuf::from(candidates[0]))
}

fn print_usage() {
    eprintln!(
        "Usage:\n  sentinel-v2-rust --version\n  sentinel-v2-rust validate-signatures --signatures <path>\n  sentinel-v2-rust scan --target <dir> --signatures <path> --json <path> --markdown <path>"
    );
}
