# Handout Note: SELinux

## Scope

This handout shows how Linux can move beyond discretionary access control by adding mandatory policy enforcement through SELinux.

## Big Picture

SELinux adds Mandatory Access Control (MAC) to Linux through:

- security contexts,
- type enforcement,
- policy rules,
- kernel hooks that consult the policy before access is granted.

Important design lesson:

- even a root-owned process is not automatically all-powerful if policy says otherwise.

## Security Contexts

SELinux labels both files and processes. The handout shows contexts as:

- user
- role
- type/domain
- level

In practice, the type or domain is often the most operationally important part because type enforcement rules are written around it.

## Type Enforcement

The core SELinux rule form is:

```text
allow source_type target_type : class perm_set;
```

Interpretation:

- source domain requests an operation
- target object has a type
- object class and permission set define what is being attempted

This is the policy layer behind statements like "httpd can read web content but cannot read arbitrary files."

## How Enforcement Happens

The slide deck includes a simplified kernel hook:

- get current process SID
- get target file context
- ask the Access Vector Cache (AVC) whether the permission is allowed

Study takeaway:

- SELinux is not an afterthought in user space; it is integrated into the kernel access path.

## Working With Policy

The handout shows a basic custom-policy workflow:

1. Write a TE policy module.
2. Install policy-development tools.
3. Compile the module.
4. Install it with `semodule`.
5. Observe denials in the audit log.
6. Use tools such as `audit2allow` carefully to help draft missing rules.

Example commands from the slides:

```bash
yum install selinux-policy selinux-policy-devel policycoreutils setools-console
semodule -i test.pp
audit2allow -i /var/log/audit/audit.log -o /tmp/mypolicy.te
```

## Relabeling And Type Transitions

Two ideas are central:

### File Relabeling

Files may need a different type from the default inherited one.

This matters because:

- access decisions depend heavily on labels,
- the "wrong" label often explains confusing denials.

### Process Type Transition

When a process executes a file, the new process type can change if policy allows it.

The handout states the transition conditions clearly:

- the file type must be executable for the source domain
- the file type must be marked as an entrypoint for the target domain
- the source domain must be allowed to transition to the target domain

Common macro:

```text
domain_auto_trans(source, target, new_type)
```

### Object Type Transition

Newly created objects normally inherit context from the parent location, but policy can choose a more specific type based on the creating process's domain.

This is how SELinux keeps object labels meaningful in multi-service systems.

## Unprivileged Root And Constrained Users

The later slides emphasize that SELinux can restrict behavior even when UNIX-level identity looks powerful.

Example shown in the handout:

```bash
semanage login -a -s user_u hank
setsebool user_ping off
```

This demonstrates that policy can limit actions such as `ping` for selected users.

## What To Remember

- SELinux is label-driven MAC, not just "extra permissions."
- Type enforcement is the day-to-day core.
- Most troubleshooting comes down to labels, domains, transitions, and audit logs.
- Root is constrained by policy, which is a major shift from classic UNIX thinking.

## Review Checklist

- Can I read a context label and identify the important pieces?
- Do I understand the structure of an `allow` rule?
- Can I explain the difference between relabeling and type transition?
- Do I know where to look when SELinux denies an action?
