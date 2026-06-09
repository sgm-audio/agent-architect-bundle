---
name: cli-open-source-tools
description: Command-line interface tools, shell scripting, system administration, developer utilities, package managers, and open source command-line applications. Use when working with terminal operations, shell commands, automation, devops tools, or CLI applications.
---

# CLI and Open Source Tooling Skills

## Shell and Terminal

### Bash
- **Scripting**: Write and execute bash scripts
- **Variables**: Variable declaration and manipulation
- **Conditionals**: If/else, case statements
- **Loops**: For, while, until loops
- **Functions**: Define and call functions
- **Arrays**: Array manipulation
- **String operations**: Substring, replacement, splitting

### Zsh
- **Oh My Zsh**: Framework for zsh configuration
- **Plugins**: Enable and configure plugins
- **Aliases**: Create command shortcuts
- **Functions**: Extended function capabilities
- **Completion**: Advanced completion system

### PowerShell
- **Cmdlets**: PowerShell commands
- **Pipelines**: Chain commands with pipes
- **Objects**: Work with .NET objects
- **Scripts**: Write .ps1 scripts
- **Modules**: Import and use modules
- **Remoting**: Remote system management

## Package Managers

### npm/yarn/pnpm
- **Install packages**: `npm install <package>`
- **Package.json**: Manage dependencies
- **Scripts**: Define npm scripts
- **Workspaces**: Monorepo support
- **Versioning**: Semantic versioning

### pip/poetry
- **Install packages**: `pip install <package>`
- **Requirements.txt**: Pin dependencies
- **Virtual environments**: Isolated environments
- **Poetry**: Modern Python packaging

### apt/dpkg
- **Install packages**: `apt install <package>`
- **Search packages**: `apt search <package>`
- **Update**: `apt update && apt upgrade`
- **Remove**: `apt remove <package>`

### Homebrew
- **Install**: `brew install <package>`
- **Search**: `brew search <package>`
- **List installed**: `brew list`
- **Cleanup**: `brew cleanup`

### Cargo (Rust)
- **Create project**: `cargo new <project>`
- **Build**: `cargo build`
- **Run**: `cargo run`
- **Test**: `cargo test`
- **Publish**: `cargo publish`

## Version Control

### Git
- **Repository init**: `git init`
- **Clone**: `git clone <url>`
- **Branching**: `git branch`, `git checkout -b`
- **Staging**: `git add`, `git rm`
- **Committing**: `git commit`
- **Remote**: `git remote add`, `git push`, `git pull`
- **Merging**: `git merge`, `git rebase`
- **Stashing**: `git stash`
- **History**: `git log`, `git diff`
- **Reset**: `git reset`, `git revert`

### GitHub CLI
- **Authentication**: `gh auth login`
- **Create repo**: `gh repo create`
- **Issues**: `gh issue create`, `gh issue list`
- **PRs**: `gh pr create`, `gh pr merge`
- **Actions**: `gh run list`, `gh run watch`

### Git Tools
- **gitk**: Visual git viewer
- **tig**: Text-mode git interface
- **gh**: GitHub CLI
- **git-flow**: Branching model

## Text Processing

### sed
- **Substitution**: `s/pattern/replacement/g`
- **Delete lines**: `/pattern/d`
- **Print lines**: `/pattern/p`
- **In-place editing**: `-i` flag

### awk
- **Field processing**: Print specific columns
- **Patterns**: `awk '/pattern/ {action}'`
- **Built-in variables**: FS, OFS, NR, NF
- **Functions**: Printf, length, substr

### grep/ripgrep
- **Basic search**: `grep "pattern" <file>`
- **Recursive**: `grep -r "pattern" <dir>`
- **Regex**: Extended regex support
- **ripgrep**: `rg` - faster alternative
- **Context**: `-A`, `-B`, `-C` for context

### jq
- **Parse JSON**: `.field`, `.field1.field2`
- **Arrays**: `.[0]`, `.[:]`, `.[]`
- **Filters**: `select()`, `map()`, `reduce()`
- **Transform**: `jq` for JSON manipulation
- **Output**: `-r` for raw output

### yq
- **Parse YAML**: Similar to jq for YAML
- **Edit YAML**: Update values
- **Convert**: JSON to YAML and back

## System Administration

### File Operations
- **ls**: List files with options
- **find**: Find files by name, type, time
- **xargs**: Build and execute commands
- **rsync**: Sync files between locations
- **scp**: Secure copy over SSH

### Process Management
- **ps**: List processes
- **top/htop**: Monitor processes
- **kill**: Terminate processes
- **systemctl**: Manage services
- **journalctl**: View logs

### Network
- **ssh**: Secure shell connections
- **scp/sftp**: File transfer
- **curl**: HTTP requests
- **wget**: Download files
- **netstat/ss**: Network statistics
- **tcpdump**: Packet capture
- **nmap**: Port scanning

### Monitoring
- **htop**: Interactive process viewer
- **iotop**: I/O monitoring
- **atop**: Advanced system monitor
- **dstat**: Resource statistics
- **glances**: Cross-platform monitoring

## Developer Tools

### Build Tools
- **make**: Build automation
- **cmake**: Cross-platform build
- **ninja**: Fast build system
- **gradle**: Java build tool

### Docker
- **Images**: `docker pull`, `docker images`
- **Containers**: `docker run`, `docker ps`, `docker stop`
- **Dockerfile**: Build custom images
- **Docker Compose**: Multi-container apps
- **Volumes**: Data persistence
- **Networking**: Container networking

### Kubernetes
- **kubectl**: Kubernetes CLI
- **Pods**: `kubectl get pods`, `kubectl describe pod`
- **Deployments**: `kubectl apply`, `kubectl rollout`
- **Services**: Expose applications
- **Config**: `kubectl config`

### Terraform/Infrastructure
- **terraform init**: Initialize
- **terraform plan**: Preview changes
- **terraform apply**: Apply changes
- **terraform destroy**: Tear down
- **terraform state**: Manage state

## CLI Applications

### Text Editors
- **vim/nvim**: Modal text editor
- **nano**: Simple text editor
- **emacs**: Extensible editor

### File Managers
- **ranger**: Terminal file manager
- **fzf**: Fuzzy finder
- **fd**: Fast find alternative
- **ripgrep**: Fast grep alternative

### Productivity
- **tmux**: Terminal multiplexer
- **screen**: Session management
- **tldr**: Simplified man pages
- **bat**: Cat with syntax highlighting
- **exa/lsd**: Modern ls replacements
- **btop/htop**: Resource monitors

### Git Helpers
- **tig**: Git interface
- **git-delta**: Syntax-highlighting pager
- **lazygit**: TUI git client
- **gh**: GitHub CLI

### API/Network Tools
- **httpie**: Human-friendly HTTP client
- **curlie**: HTTP client with curl ease
- **Postman CLI**: API testing
- **grpcurl**: gRPC debugging

### Data Tools
- **csvkit**: CSV processing
- **Miller**: CSV/JSON/TSV processing
- **xsv**: Fast CSV indexer
- **sqlite3**: SQLite CLI

## Shell Customization

### dotfiles
- **Shell config**: .bashrc, .zshrc, .bash_profile
- **Aliases**: Custom command shortcuts
- **Functions**: Shell functions
- **Prompt**: Custom prompt (PS1)
- **Variables**: Environment variables

### Terminal Emulators
- **iTerm2**: macOS terminal
- **Alacritty**: GPU-accelerated
- **Kitty**: Fast, feature-rich
- **Windows Terminal**: Windows terminal

### Tool Configuration
- **EditorConfig**: Code style standardization
- **Shellcheck**: Bash linting
- **Shell formatting**: shfmt

## Automation

### Cron Jobs
- **Crontab**: Schedule tasks
- **Syntax**: Minute, hour, day, month, weekday
- **Environment**: Set PATH in crontab

### systemd Timers
- **Timer units**: Time-based triggers
- **Service units**: Work to perform
- **Management**: systemctl commands

### Scripts
- **Shebang**: Script header
- **Error handling**: set -e, trap
- **Logging**: Log to files
- **Arguments**: Parse command line args

## Security

### SSH
- **Key generation**: `ssh-keygen`
- **Config**: ~/.ssh/config
- **Agent**: SSH agent for keys
- **Tunneling**: Port forwarding

### GPG
- **Key management**: Generate, list, export
- **Signing**: Sign commits, files
- **Encryption**: Encrypt/decrypt files

### Password Management
- **pass**: CLI password manager
- **gopass**: Team password management

## Troubleshooting

### Debugging
- **Shell tracing**: `set -x` for debug
- **Check exit codes**: `$?`
- **Validate input**: Input sanitization

### Performance
- **Time commands**: `time` or `hyperfine`
- **Profile scripts**: bash profiler
- **Optimize loops**: Avoid subshells

### Common Issues
- **Permission denied**: chmod, sudo
- **Command not found**: Check PATH
- **No space left**: df, du
- **Process conflicts**: Kill conflicting processes
