use std::collections::HashMap;
use std::fs;
use std::path::{Path, PathBuf};

use chrono::{SecondsFormat, Utc};
use serde::Serialize;
use sha2::{Digest, Sha256};

use crate::patterns::PatternEngine;
use crate::signatures::{severity_rank, HashSignatureMatcher, SignatureDatabase};

const SYMLINK_SKIP_REASON: &str =
    "Symbolic link skipped to keep scans inside the explicit target tree.";

#[derive(Debug, Clone, Serialize)]
pub struct Report {
    pub tool: String,
    pub signature_schema_version: String,
    pub started_at: String,
    pub finished_at: String,
    pub target: String,
    pub scan_metadata: ScanMetadata,
    pub summary: Summary,
    pub findings: Vec<FileResult>,
    pub all_results: Vec<FileResult>,
}

#[derive(Debug, Clone, Serialize)]
pub struct ScanMetadata {
    pub hash_filter: String,
    pub hash_filter_items: usize,
    pub hash_filter_bits: usize,
    pub hash_filter_hash_functions: usize,
    pub hash_filter_policy: String,
    pub pattern_engine: String,
    pub pattern_count: usize,
    pub automaton_states: usize,
    pub traversal_policy: String,
    pub symlink_policy: String,
}

#[derive(Debug, Clone, Serialize, Default)]
pub struct Summary {
    pub infected: usize,
    pub suspicious: usize,
    pub clean: usize,
    pub skipped: usize,
    pub error: usize,
    pub files_scanned: usize,
    pub total_results: usize,
}

#[derive(Debug, Clone, Serialize)]
pub struct FileResult {
    pub path: String,
    pub status: String,
    pub severity: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub size_bytes: Option<u64>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub md5: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub sha256: Option<String>,
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub matches: Vec<SignatureMatch>,
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub heuristics: Vec<HeuristicFinding>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub skip_reason: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub error: Option<String>,
}

#[derive(Debug, Clone, Serialize)]
pub struct SignatureMatch {
    pub signature_id: String,
    pub signature_name: String,
    pub category: String,
    pub severity: String,
    pub matcher: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub pattern_bytes: Option<usize>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub pattern_offset: Option<usize>,
}

#[derive(Debug, Clone, Serialize)]
pub struct HeuristicFinding {
    pub rule_id: String,
    pub severity: String,
    pub description: String,
    pub evidence: String,
}

pub fn scan_directory(target: &Path, database: &SignatureDatabase) -> Result<Report, String> {
    let started_at = timestamp();
    let pattern_engine = PatternEngine::new(database.patterns.clone());
    let metadata = ScanMetadata {
        hash_filter: "bloom-filter".to_string(),
        hash_filter_items: database.hash_filter.items(),
        hash_filter_bits: database.hash_filter.bit_count(),
        hash_filter_hash_functions: database.hash_filter.hash_functions(),
        hash_filter_policy: "precheck-then-exact-hash-map".to_string(),
        pattern_engine: "aho-corasick-byte-automaton".to_string(),
        pattern_count: pattern_engine.pattern_count(),
        automaton_states: pattern_engine.state_count(),
        traversal_policy: "deterministic-recursive-files".to_string(),
        symlink_policy: "skip".to_string(),
    };

    let mut results = Vec::new();
    let root_metadata = match fs::symlink_metadata(target) {
        Ok(metadata) => metadata,
        Err(_) => {
            results.push(FileResult {
                path: target.display().to_string(),
                status: "error".to_string(),
                severity: "high".to_string(),
                size_bytes: None,
                md5: None,
                sha256: None,
                matches: Vec::new(),
                heuristics: Vec::new(),
                skip_reason: None,
                error: Some("Target path does not exist.".to_string()),
            });
            return Ok(build_report(
                target,
                started_at,
                timestamp(),
                database,
                metadata,
                results,
            ));
        }
    };

    if root_metadata.file_type().is_symlink() {
        results.push(skipped_result(target.display().to_string()));
    } else if root_metadata.is_file() {
        results.push(scan_file(target, target, database, &pattern_engine));
    } else {
        for path in collect_paths(target)? {
            let metadata = fs::symlink_metadata(&path)
                .map_err(|err| format!("could not read metadata for {}: {err}", path.display()))?;
            if metadata.file_type().is_symlink() {
                results.push(skipped_result(display_path(&path, target)));
            } else if metadata.is_file() {
                results.push(scan_file(&path, target, database, &pattern_engine));
            }
        }
    }

    Ok(build_report(
        target,
        started_at,
        timestamp(),
        database,
        metadata,
        results,
    ))
}

fn scan_file(
    path: &Path,
    root: &Path,
    database: &SignatureDatabase,
    pattern_engine: &PatternEngine,
) -> FileResult {
    let display = display_path(path, root);
    let content = match fs::read(path) {
        Ok(content) => content,
        Err(err) => {
            return FileResult {
                path: display,
                status: "error".to_string(),
                severity: "medium".to_string(),
                size_bytes: None,
                md5: None,
                sha256: None,
                matches: Vec::new(),
                heuristics: Vec::new(),
                skip_reason: None,
                error: Some(err.to_string()),
            }
        }
    };

    let md5_hex = format!("{:x}", md5::compute(&content));
    let mut sha256 = Sha256::new();
    sha256.update(&content);
    let sha256_hex = format!("{:x}", sha256.finalize());
    let mut hashes = HashMap::new();
    hashes.insert("md5".to_string(), md5_hex.clone());
    hashes.insert("sha256".to_string(), sha256_hex.clone());

    let mut matches = Vec::new();
    for hash_matcher in find_hash_matches(&hashes, database) {
        matches.push(hash_match_to_report(&hash_matcher));
    }
    for pattern_match in pattern_engine.scan(&content) {
        matches.push(SignatureMatch {
            signature_id: pattern_match.signature.id,
            signature_name: pattern_match.signature.name,
            category: pattern_match.signature.category,
            severity: pattern_match.signature.severity,
            matcher: pattern_match.matcher,
            pattern_bytes: Some(pattern_match.pattern_bytes),
            pattern_offset: Some(pattern_match.pattern_offset),
        });
    }

    let heuristics = run_heuristics(&content);
    let (status, severity) = if matches.is_empty() {
        if heuristics.is_empty() {
            ("clean".to_string(), "info".to_string())
        } else {
            (
                "suspicious".to_string(),
                highest_severity(heuristics.iter().map(|finding| finding.severity.as_str())),
            )
        }
    } else {
        (
            "infected".to_string(),
            highest_severity(matches.iter().map(|finding| finding.severity.as_str())),
        )
    };

    FileResult {
        path: display,
        status,
        severity,
        size_bytes: Some(content.len() as u64),
        md5: Some(md5_hex),
        sha256: Some(sha256_hex),
        matches,
        heuristics,
        skip_reason: None,
        error: None,
    }
}

fn find_hash_matches(
    hashes: &HashMap<String, String>,
    database: &SignatureDatabase,
) -> Vec<HashSignatureMatcher> {
    let mut matches = Vec::new();
    for (algorithm, digest) in hashes {
        if !database.hash_filter.might_contain(algorithm, digest) {
            continue;
        }
        if let Some(digest_map) = database.hash_index.get(algorithm) {
            if let Some(found) = digest_map.get(digest) {
                matches.extend(found.iter().cloned());
            }
        }
    }
    matches
}

fn hash_match_to_report(hash_matcher: &HashSignatureMatcher) -> SignatureMatch {
    SignatureMatch {
        signature_id: hash_matcher.signature.id.clone(),
        signature_name: hash_matcher.signature.name.clone(),
        category: hash_matcher.signature.category.clone(),
        severity: hash_matcher.signature.severity.clone(),
        matcher: hash_matcher.matcher_type.clone(),
        pattern_bytes: None,
        pattern_offset: None,
    }
}

fn run_heuristics(content: &[u8]) -> Vec<HeuristicFinding> {
    let sample_len = content.len().min(1024 * 1024);
    let text = String::from_utf8_lossy(&content[..sample_len]);
    let indicators: Vec<&str> = ["CreateRemoteThread", "VirtualAllocEx", "WriteProcessMemory"]
        .into_iter()
        .filter(|indicator| text.contains(indicator))
        .collect();

    if indicators.is_empty() {
        Vec::new()
    } else {
        vec![HeuristicFinding {
            rule_id: "api-name-indicator".to_string(),
            severity: "medium".to_string(),
            description: "Suspicious API-name strings appear in the file.".to_string(),
            evidence: indicators.join(", "),
        }]
    }
}

fn build_report(
    target: &Path,
    started_at: String,
    finished_at: String,
    database: &SignatureDatabase,
    scan_metadata: ScanMetadata,
    results: Vec<FileResult>,
) -> Report {
    let summary = summarize(&results);
    let findings = results
        .iter()
        .filter(|result| matches!(result.status.as_str(), "infected" | "suspicious" | "skipped" | "error"))
        .cloned()
        .collect();

    Report {
        tool: "Sentinel v2 Rust".to_string(),
        signature_schema_version: database.schema_version.clone(),
        started_at,
        finished_at,
        target: target.display().to_string(),
        scan_metadata,
        summary,
        findings,
        all_results: results,
    }
}

fn summarize(results: &[FileResult]) -> Summary {
    let mut summary = Summary::default();
    for result in results {
        match result.status.as_str() {
            "infected" => summary.infected += 1,
            "suspicious" => summary.suspicious += 1,
            "clean" => summary.clean += 1,
            "skipped" => summary.skipped += 1,
            "error" => summary.error += 1,
            _ => {}
        }
    }
    summary.files_scanned = results
        .iter()
        .filter(|result| !matches!(result.status.as_str(), "skipped" | "error"))
        .count();
    summary.total_results = results.len();
    summary
}

fn collect_paths(root: &Path) -> Result<Vec<PathBuf>, String> {
    let mut paths = Vec::new();
    collect_paths_inner(root, &mut paths)?;
    paths.sort();
    Ok(paths)
}

fn collect_paths_inner(root: &Path, paths: &mut Vec<PathBuf>) -> Result<(), String> {
    let mut entries = fs::read_dir(root)
        .map_err(|err| format!("could not read directory {}: {err}", root.display()))?
        .collect::<Result<Vec<_>, _>>()
        .map_err(|err| format!("could not read directory entry under {}: {err}", root.display()))?;
    entries.sort_by_key(|entry| entry.path());

    for entry in entries {
        let path = entry.path();
        let metadata = fs::symlink_metadata(&path)
            .map_err(|err| format!("could not read metadata for {}: {err}", path.display()))?;
        if metadata.file_type().is_symlink() || metadata.is_file() {
            paths.push(path);
        } else if metadata.is_dir() {
            collect_paths_inner(&path, paths)?;
        }
    }
    Ok(())
}

fn skipped_result(path: String) -> FileResult {
    FileResult {
        path,
        status: "skipped".to_string(),
        severity: "info".to_string(),
        size_bytes: None,
        md5: None,
        sha256: None,
        matches: Vec::new(),
        heuristics: Vec::new(),
        skip_reason: Some(SYMLINK_SKIP_REASON.to_string()),
        error: None,
    }
}

fn display_path(path: &Path, root: &Path) -> String {
    let base = if root.is_dir() {
        root
    } else {
        root.parent().unwrap_or(root)
    };
    path.strip_prefix(base)
        .unwrap_or(path)
        .to_string_lossy()
        .replace('\\', "/")
}

fn highest_severity<'a>(values: impl Iterator<Item = &'a str>) -> String {
    values
        .max_by_key(|value| severity_rank(*value))
        .unwrap_or("info")
        .to_string()
}

fn timestamp() -> String {
    Utc::now().to_rfc3339_opts(SecondsFormat::Secs, true)
}
