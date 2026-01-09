# Set up Claude Code

> Install, authenticate, and start using Claude Code on your development machine.

## System requirements

- **Operating Systems**: macOS 10.15+, Ubuntu 20.04+/Debian 10+, or Windows 10+ (with WSL 1, WSL 2, or Git for Windows)
- **Hardware**: 4GB+ RAM
- **Software**: [Node.js 18+](https://nodejs.org/en/download)
- **Network**: Internet connection required for authentication and AI processing
- **Shell**: Works best in Bash, Zsh or Fish
- **Location**: [Anthropic supported countries](https://www.anthropic.com/supported-countries)

## Standard installation

To install Claude Code, run the following command:

```sh
npm install -g @anthropic-ai/claude-code
```

<Warning>
  Do NOT use `sudo npm install -g` as this can lead to permission issues and security risks.
  If you encounter permission errors, see [configure Claude Code](/en/docs/claude-code/troubleshooting#linux-permission-issues) for recommended solutions.
</Warning>

<Note>
  Some users may be automatically migrated to an improved installation method.
  Run `claude doctor` after installation to check your installation type.
</Note>

After the installation process completes, navigate to your project and start Claude Code:

```bash
cd your-awesome-project
claude
```

Claude Code offers the following authentication options:

1. **Anthropic Console**: The default option. Connect through the Anthropic Console and complete the OAuth process. Requires active billing at [console.anthropic.com](https://console.anthropic.com).
2. **Claude App (with Pro or Max plan)**: Subscribe to Claude's [Pro or Max plan](https://www.anthropic.com/pricing) for a unified subscription that includes both Claude Code and the web interface. Get more value at the same price point while managing your account in one place. Log in with your Claude.ai account. During launch, choose the option that matches your subscription type.
3. **Enterprise platforms**: Configure Claude Code to use [Amazon Bedrock or Google Vertex AI](/en/docs/claude-code/third-party-integrations) for enterprise deployments with your existing cloud infrastructure.

<Note>
  Claude Code securely stores your credentials. See [Credential Management](/en/docs/claude-code/iam#credential-management) for details.
</Note>

## Windows setup

**Option 1: Claude Code within WSL**

- Both WSL 1 and WSL 2 are supported

**Option 2: Claude Code on native Windows with Git Bash**

- Requires [Git for Windows](https://git-scm.com/downloads/win)
- For portable Git installations, specify the path to your `bash.exe`:
  ```powershell
  $env:CLAUDE_CODE_GIT_BASH_PATH="C:\Program Files\Git\bin\bash.exe"
  ```

## Alternative installation methods

Claude Code offers multiple installation methods to suit different environments.

If you encounter any issues during installation, consult the [troubleshooting guide](/en/docs/claude-code/troubleshooting#linux-permission-issues).

<Tip>
  Run `claude doctor` after installation to check your installation type and version.
</Tip>

### Global npm installation

Traditional method shown in the [install steps above](#install-and-authenticate)

### Native binary installation (Beta)

If you have an existing installation of Claude Code, use `claude install` to start the native binary installation.

For a fresh install, run the following command:

**macOS, Linux, WSL:**

```bash
# Install stable version (default)
curl -fsSL https://claude.ai/install.sh | bash

# Install latest version
curl -fsSL https://claude.ai/install.sh | bash -s latest

# Install specific version number
curl -fsSL https://claude.ai/install.sh | bash -s 1.0.58
```

**Windows PowerShell:**

```powershell
# Install stable version (default)
irm https://claude.ai/install.ps1 | iex

# Install latest version
& ([scriptblock]::Create((irm https://claude.ai/install.ps1))) latest

# Install specific version number
& ([scriptblock]::Create((irm https://claude.ai/install.ps1))) 1.0.58

```

The native Claude Code installer is supported on macOS, Linux, and Windows.

<Tip>
  Make sure that you remove any outdated aliases or symlinks.
  Once your installation is complete, run `claude doctor` to verify the installation.
</Tip>

### Local installation

- After global install via npm, use `claude migrate-installer` to move to local
- Avoids autoupdater npm permission issues
- Some users may be automatically migrated to this method

## Running on AWS or GCP

By default, Claude Code uses Anthropic's API.

For details on running Claude Code on AWS or GCP, see [third-party integrations](/en/docs/claude-code/third-party-integrations).

## Update Claude Code

### Auto updates

Claude Code automatically keeps itself up to date to ensure you have the latest features and security fixes.

- **Update checks**: Performed on startup and periodically while running
- **Update process**: Downloads and installs automatically in the background
- **Notifications**: You'll see a notification when updates are installed
- **Applying updates**: Updates take effect the next time you start Claude Code

**Disable auto-updates:**

```bash
# Via configuration
claude config set autoUpdates false --global

# Or via environment variable
export DISABLE_AUTOUPDATER=1
```

### Update manually

```bash
claude update
```

# Set up Claude Code

> Install, authenticate, and start using Claude Code on your development machine.

## System requirements

- **Operating Systems**: macOS 10.15+, Ubuntu 20.04+/Debian 10+, or Windows 10+ (with WSL 1, WSL 2, or Git for Windows)
- **Hardware**: 4GB+ RAM
- **Software**: [Node.js 18+](https://nodejs.org/en/download)
- **Network**: Internet connection required for authentication and AI processing
- **Shell**: Works best in Bash, Zsh or Fish
- **Location**: [Anthropic supported countries](https://www.anthropic.com/supported-countries)

## Standard installation

To install Claude Code, run the following command:

```sh
npm install -g @anthropic-ai/claude-code
```

<Warning>
  Do NOT use `sudo npm install -g` as this can lead to permission issues and security risks.
  If you encounter permission errors, see [configure Claude Code](/en/docs/claude-code/troubleshooting#linux-permission-issues) for recommended solutions.
</Warning>

<Note>
  Some users may be automatically migrated to an improved installation method.
  Run `claude doctor` after installation to check your installation type.
</Note>

After the installation process completes, navigate to your project and start Claude Code:

```bash
cd your-awesome-project
claude
```

Claude Code offers the following authentication options:

1. **Anthropic Console**: The default option. Connect through the Anthropic Console and complete the OAuth process. Requires active billing at [console.anthropic.com](https://console.anthropic.com).
2. **Claude App (with Pro or Max plan)**: Subscribe to Claude's [Pro or Max plan](https://www.anthropic.com/pricing) for a unified subscription that includes both Claude Code and the web interface. Get more value at the same price point while managing your account in one place. Log in with your Claude.ai account. During launch, choose the option that matches your subscription type.
3. **Enterprise platforms**: Configure Claude Code to use [Amazon Bedrock or Google Vertex AI](/en/docs/claude-code/third-party-integrations) for enterprise deployments with your existing cloud infrastructure.

<Note>
  Claude Code securely stores your credentials. See [Credential Management](/en/docs/claude-code/iam#credential-management) for details.
</Note>

## Windows setup

**Option 1: Claude Code within WSL**

- Both WSL 1 and WSL 2 are supported

**Option 2: Claude Code on native Windows with Git Bash**

- Requires [Git for Windows](https://git-scm.com/downloads/win)
- For portable Git installations, specify the path to your `bash.exe`:
  ```powershell
  $env:CLAUDE_CODE_GIT_BASH_PATH="C:\Program Files\Git\bin\bash.exe"
  ```

## Alternative installation methods

Claude Code offers multiple installation methods to suit different environments.

If you encounter any issues during installation, consult the [troubleshooting guide](/en/docs/claude-code/troubleshooting#linux-permission-issues).

<Tip>
  Run `claude doctor` after installation to check your installation type and version.
</Tip>

### Global npm installation

Traditional method shown in the [install steps above](#install-and-authenticate)

### Native binary installation (Beta)

If you have an existing installation of Claude Code, use `claude install` to start the native binary installation.

For a fresh install, run the following command:

**macOS, Linux, WSL:**

```bash
# Install stable version (default)
curl -fsSL https://claude.ai/install.sh | bash

# Install latest version
curl -fsSL https://claude.ai/install.sh | bash -s latest

# Install specific version number
curl -fsSL https://claude.ai/install.sh | bash -s 1.0.58
```

**Windows PowerShell:**

```powershell
# Install stable version (default)
irm https://claude.ai/install.ps1 | iex

# Install latest version
& ([scriptblock]::Create((irm https://claude.ai/install.ps1))) latest

# Install specific version number
& ([scriptblock]::Create((irm https://claude.ai/install.ps1))) 1.0.58

```

The native Claude Code installer is supported on macOS, Linux, and Windows.

<Tip>
  Make sure that you remove any outdated aliases or symlinks.
  Once your installation is complete, run `claude doctor` to verify the installation.
</Tip>

### Local installation

- After global install via npm, use `claude migrate-installer` to move to local
- Avoids autoupdater npm permission issues
- Some users may be automatically migrated to this method

## Running on AWS or GCP

By default, Claude Code uses Anthropic's API.

For details on running Claude Code on AWS or GCP, see [third-party integrations](/en/docs/claude-code/third-party-integrations).

## Update Claude Code

### Auto updates

Claude Code automatically keeps itself up to date to ensure you have the latest features and security fixes.

- **Update checks**: Performed on startup and periodically while running
- **Update process**: Downloads and installs automatically in the background
- **Notifications**: You'll see a notification when updates are installed
- **Applying updates**: Updates take effect the next time you start Claude Code

**Disable auto-updates:**

```bash
# Via configuration
claude config set autoUpdates false --global

# Or via environment variable
export DISABLE_AUTOUPDATER=1
```

### Update manually

```bash
claude update
```

# Set up Claude Code

> Install, authenticate, and start using Claude Code on your development machine.

## System requirements

- **Operating Systems**: macOS 10.15+, Ubuntu 20.04+/Debian 10+, or Windows 10+ (with WSL 1, WSL 2, or Git for Windows)
- **Hardware**: 4GB+ RAM
- **Software**: [Node.js 18+](https://nodejs.org/en/download)
- **Network**: Internet connection required for authentication and AI processing
- **Shell**: Works best in Bash, Zsh or Fish
- **Location**: [Anthropic supported countries](https://www.anthropic.com/supported-countries)

## Standard installation

To install Claude Code, run the following command:

```sh
npm install -g @anthropic-ai/claude-code
```

<Warning>
  Do NOT use `sudo npm install -g` as this can lead to permission issues and security risks.
  If you encounter permission errors, see [configure Claude Code](/en/docs/claude-code/troubleshooting#linux-permission-issues) for recommended solutions.
</Warning>

<Note>
  Some users may be automatically migrated to an improved installation method.
  Run `claude doctor` after installation to check your installation type.
</Note>

After the installation process completes, navigate to your project and start Claude Code:

```bash
cd your-awesome-project
claude
```

Claude Code offers the following authentication options:

1. **Anthropic Console**: The default option. Connect through the Anthropic Console and complete the OAuth process. Requires active billing at [console.anthropic.com](https://console.anthropic.com).
2. **Claude App (with Pro or Max plan)**: Subscribe to Claude's [Pro or Max plan](https://www.anthropic.com/pricing) for a unified subscription that includes both Claude Code and the web interface. Get more value at the same price point while managing your account in one place. Log in with your Claude.ai account. During launch, choose the option that matches your subscription type.
3. **Enterprise platforms**: Configure Claude Code to use [Amazon Bedrock or Google Vertex AI](/en/docs/claude-code/third-party-integrations) for enterprise deployments with your existing cloud infrastructure.

<Note>
  Claude Code securely stores your credentials. See [Credential Management](/en/docs/claude-code/iam#credential-management) for details.
</Note>

## Windows setup

**Option 1: Claude Code within WSL**

- Both WSL 1 and WSL 2 are supported

**Option 2: Claude Code on native Windows with Git Bash**

- Requires [Git for Windows](https://git-scm.com/downloads/win)
- For portable Git installations, specify the path to your `bash.exe`:
  ```powershell
  $env:CLAUDE_CODE_GIT_BASH_PATH="C:\Program Files\Git\bin\bash.exe"
  ```

## Alternative installation methods

Claude Code offers multiple installation methods to suit different environments.

If you encounter any issues during installation, consult the [troubleshooting guide](/en/docs/claude-code/troubleshooting#linux-permission-issues).

<Tip>
  Run `claude doctor` after installation to check your installation type and version.
</Tip>

### Global npm installation

Traditional method shown in the [install steps above](#install-and-authenticate)

### Native binary installation (Beta)

If you have an existing installation of Claude Code, use `claude install` to start the native binary installation.

For a fresh install, run the following command:

**macOS, Linux, WSL:**

```bash
# Install stable version (default)
curl -fsSL https://claude.ai/install.sh | bash

# Install latest version
curl -fsSL https://claude.ai/install.sh | bash -s latest

# Install specific version number
curl -fsSL https://claude.ai/install.sh | bash -s 1.0.58
```

**Windows PowerShell:**

```powershell
# Install stable version (default)
irm https://claude.ai/install.ps1 | iex

# Install latest version
& ([scriptblock]::Create((irm https://claude.ai/install.ps1))) latest

# Install specific version number
& ([scriptblock]::Create((irm https://claude.ai/install.ps1))) 1.0.58

```

The native Claude Code installer is supported on macOS, Linux, and Windows.

<Tip>
  Make sure that you remove any outdated aliases or symlinks.
  Once your installation is complete, run `claude doctor` to verify the installation.
</Tip>

### Local installation

- After global install via npm, use `claude migrate-installer` to move to local
- Avoids autoupdater npm permission issues
- Some users may be automatically migrated to this method

## Running on AWS or GCP

By default, Claude Code uses Anthropic's API.

For details on running Claude Code on AWS or GCP, see [third-party integrations](/en/docs/claude-code/third-party-integrations).

## Update Claude Code

### Auto updates

Claude Code automatically keeps itself up to date to ensure you have the latest features and security fixes.

- **Update checks**: Performed on startup and periodically while running
- **Update process**: Downloads and installs automatically in the background
- **Notifications**: You'll see a notification when updates are installed
- **Applying updates**: Updates take effect the next time you start Claude Code

**Disable auto-updates:**

```bash
# Via configuration
claude config set autoUpdates false --global

# Or via environment variable
export DISABLE_AUTOUPDATER=1
```

### Update manually

```bash
claude update
```

# Set up Claude Code

> Install, authenticate, and start using Claude Code on your development machine.

## System requirements

- **Operating Systems**: macOS 10.15+, Ubuntu 20.04+/Debian 10+, or Windows 10+ (with WSL 1, WSL 2, or Git for Windows)
- **Hardware**: 4GB+ RAM
- **Software**: [Node.js 18+](https://nodejs.org/en/download)
- **Network**: Internet connection required for authentication and AI processing
- **Shell**: Works best in Bash, Zsh or Fish
- **Location**: [Anthropic supported countries](https://www.anthropic.com/supported-countries)

## Standard installation

To install Claude Code, run the following command:

```sh
npm install -g @anthropic-ai/claude-code
```

<Warning>
  Do NOT use `sudo npm install -g` as this can lead to permission issues and security risks.
  If you encounter permission errors, see [configure Claude Code](/en/docs/claude-code/troubleshooting#linux-permission-issues) for recommended solutions.
</Warning>

<Note>
  Some users may be automatically migrated to an improved installation method.
  Run `claude doctor` after installation to check your installation type.
</Note>

After the installation process completes, navigate to your project and start Claude Code:

```bash
cd your-awesome-project
claude
```

Claude Code offers the following authentication options:

1. **Anthropic Console**: The default option. Connect through the Anthropic Console and complete the OAuth process. Requires active billing at [console.anthropic.com](https://console.anthropic.com).
2. **Claude App (with Pro or Max plan)**: Subscribe to Claude's [Pro or Max plan](https://www.anthropic.com/pricing) for a unified subscription that includes both Claude Code and the web interface. Get more value at the same price point while managing your account in one place. Log in with your Claude.ai account. During launch, choose the option that matches your subscription type.
3. **Enterprise platforms**: Configure Claude Code to use [Amazon Bedrock or Google Vertex AI](/en/docs/claude-code/third-party-integrations) for enterprise deployments with your existing cloud infrastructure.

<Note>
  Claude Code securely stores your credentials. See [Credential Management](/en/docs/claude-code/iam#credential-management) for details.
</Note>

## Windows setup

**Option 1: Claude Code within WSL**

- Both WSL 1 and WSL 2 are supported

**Option 2: Claude Code on native Windows with Git Bash**

- Requires [Git for Windows](https://git-scm.com/downloads/win)
- For portable Git installations, specify the path to your `bash.exe`:
  ```powershell
  $env:CLAUDE_CODE_GIT_BASH_PATH="C:\Program Files\Git\bin\bash.exe"
  ```

## Alternative installation methods

Claude Code offers multiple installation methods to suit different environments.

If you encounter any issues during installation, consult the [troubleshooting guide](/en/docs/claude-code/troubleshooting#linux-permission-issues).

<Tip>
  Run `claude doctor` after installation to check your installation type and version.
</Tip>

### Global npm installation

Traditional method shown in the [install steps above](#install-and-authenticate)

### Native binary installation (Beta)

If you have an existing installation of Claude Code, use `claude install` to start the native binary installation.

For a fresh install, run the following command:

**macOS, Linux, WSL:**

```bash
# Install stable version (default)
curl -fsSL https://claude.ai/install.sh | bash

# Install latest version
curl -fsSL https://claude.ai/install.sh | bash -s latest

# Install specific version number
curl -fsSL https://claude.ai/install.sh | bash -s 1.0.58
```

**Windows PowerShell:**

```powershell
# Install stable version (default)
irm https://claude.ai/install.ps1 | iex

# Install latest version
& ([scriptblock]::Create((irm https://claude.ai/install.ps1))) latest

# Install specific version number
& ([scriptblock]::Create((irm https://claude.ai/install.ps1))) 1.0.58

```

The native Claude Code installer is supported on macOS, Linux, and Windows.

<Tip>
  Make sure that you remove any outdated aliases or symlinks.
  Once your installation is complete, run `claude doctor` to verify the installation.
</Tip>

### Local installation

- After global install via npm, use `claude migrate-installer` to move to local
- Avoids autoupdater npm permission issues
- Some users may be automatically migrated to this method

## Running on AWS or GCP

By default, Claude Code uses Anthropic's API.

For details on running Claude Code on AWS or GCP, see [third-party integrations](/en/docs/claude-code/third-party-integrations).

## Update Claude Code

### Auto updates

Claude Code automatically keeps itself up to date to ensure you have the latest features and security fixes.

- **Update checks**: Performed on startup and periodically while running
- **Update process**: Downloads and installs automatically in the background
- **Notifications**: You'll see a notification when updates are installed
- **Applying updates**: Updates take effect the next time you start Claude Code

**Disable auto-updates:**

```bash
# Via configuration
claude config set autoUpdates false --global

# Or via environment variable
export DISABLE_AUTOUPDATER=1
```

### Update manually

```bash
claude update
```
