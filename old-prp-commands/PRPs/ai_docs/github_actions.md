# Claude Code GitHub Actions

> Learn about integrating Claude Code into your development workflow with Claude Code GitHub Actions

Claude Code GitHub Actions brings AI-powered automation to your GitHub workflow. With a simple `@claude` mention in any PR or issue, Claude can analyze your code, create pull requests, implement features, and fix bugs - all while following your project's standards.

<Info>
  Claude Code GitHub Actions is currently in beta. Features and functionality may evolve as we refine the experience.
</Info>

<Note>
  Claude Code GitHub Actions is built on top of the [Claude Code SDK](/en/docs/claude-code/sdk), which enables programmatic integration of Claude Code into your applications. You can use the SDK to build custom automation workflows beyond GitHub Actions.
</Note>

## Why use Claude Code GitHub Actions?

- **Instant PR creation**: Describe what you need, and Claude creates a complete PR with all necessary changes
- **Automated code implementation**: Turn issues into working code with a single command
- **Follows your standards**: Claude respects your `CLAUDE.md` guidelines and existing code patterns
- **Simple setup**: Get started in minutes with our installer and API key
- **Secure by default**: Your code stays on Github's runners

## What can Claude do?

Claude Code provides powerful GitHub Actions that transform how you work with code:

### Claude Code Action

This GitHub Action allows you to run Claude Code within your GitHub Actions workflows. You can use this to build any custom workflow on top of Claude Code.

[View repository →](https://github.com/anthropics/claude-code-action)

### Claude Code Action (Base)

The foundation for building custom GitHub workflows with Claude. This extensible framework gives you full access to Claude's capabilities for creating tailored automation.

[View repository →](https://github.com/anthropics/claude-code-base-action)

## Setup

## Quick setup

The easiest way to set up this action is through Claude Code in the terminal. Just open claude and run `/install-github-app`.

This command will guide you through setting up the GitHub app and required secrets.

<Note>
  * You must be a repository admin to install the GitHub app and add secrets
  * This quickstart method is only available for direct Anthropic API users. If you're using AWS Bedrock or Google Vertex AI, please see the [Using with AWS Bedrock & Google Vertex AI](#using-with-aws-bedrock-%26-google-vertex-ai) section.
</Note>

## Manual setup

If the `/install-github-app` command fails or you prefer manual setup, please follow these manual setup instructions:

1. **Install the Claude GitHub app** to your repository: [https://github.com/apps/claude](https://github.com/apps/claude)
2. **Add ANTHROPIC_API_KEY** to your repository secrets ([Learn how to use secrets in GitHub Actions](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions))
3. **Copy the workflow file** from [examples/claude.yml](https://github.com/anthropics/claude-code-action/blob/main/examples/claude.yml) into your repository's `.github/workflows/`

<Tip>
  After completing either the quickstart or manual setup, test the action by tagging `@claude` in an issue or PR comment!
</Tip>

## Example use cases

Claude Code GitHub Actions can help you with a variety of tasks. For complete working examples, see the [examples directory](https://github.com/anthropics/claude-code-action/tree/main/examples).

### Turn issues into PRs

In an issue comment:

```
@claude implement this feature based on the issue description
```

Claude will analyze the issue, write the code, and create a PR for review.

### Get implementation help

In a PR comment:

```
@claude how should I implement user authentication for this endpoint?
```

Claude will analyze your code and provide specific implementation guidance.

### Fix bugs quickly

In an issue:

```yaml
@claude fix the TypeError in the user dashboard component
```

Claude will locate the bug, implement a fix, and create a PR.

## Best practices

### CLAUDE.md configuration

Create a `CLAUDE.md` file in your repository root to define code style guidelines, review criteria, project-specific rules, and preferred patterns. This file guides Claude's understanding of your project standards.

### Security considerations

<Warning>
  Never commit API keys directly to your repository!
</Warning>

Always use GitHub Secrets for API keys:

- Add your API key as a repository secret named `ANTHROPIC_API_KEY`
- Reference it in workflows: `anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}`
- Limit action permissions to only what's necessary
- Review Claude's suggestions before merging

Always use GitHub Secrets (e.g., `${{ secrets.ANTHROPIC_API_KEY }}`) rather than hardcoding API keys directly in your workflow files.

### Optimizing performance

Use issue templates to provide context, keep your `CLAUDE.md` concise and focused, and configure appropriate timeouts for your workflows.

### CI costs

When using Claude Code GitHub Actions, be aware of the associated costs:

**GitHub Actions costs:**

- Claude Code runs on GitHub-hosted runners, which consume your GitHub Actions minutes
- See [GitHub's billing documentation](https://docs.github.com/en/billing/managing-billing-for-your-products/managing-billing-for-github-actions/about-billing-for-github-actions) for detailed pricing and minute limits

**API costs:**

- Each Claude interaction consumes API tokens based on the length of prompts and responses
- Token usage varies by task complexity and codebase size
- See [Claude's pricing page](https://www.anthropic.com/api) for current token rates

**Cost optimization tips:**

- Use specific `@claude` commands to reduce unnecessary API calls
- Configure appropriate `max_turns` limits to prevent excessive iterations
- Set reasonable `timeout_minutes` to avoid runaway workflows
- Consider using GitHub's concurrency controls to limit parallel runs

## Configuration examples

For ready-to-use workflow configurations for different use cases, including:

- Basic workflow setup for issue and PR comments
- Automated code reviews on pull requests
- Custom implementations for specific needs

Visit the [examples directory](https://github.com/anthropics/claude-code-action/tree/main/examples) in the Claude Code Action repository.

<Tip>
  The examples repository includes complete, tested workflows that you can copy directly into your `.github/workflows/` directory.
</Tip>

## Using with AWS Bedrock & Google Vertex AI

For enterprise environments, you can use Claude Code GitHub Actions with your own cloud infrastructure. This approach gives you control over data residency and billing while maintaining the same functionality.

### Prerequisites

Before setting up Claude Code GitHub Actions with cloud providers, you need:

#### For Google Cloud Vertex AI:

1. A Google Cloud Project with Vertex AI enabled
2. Workload Identity Federation configured for GitHub Actions
3. A service account with the required permissions
4. A GitHub App (recommended) or use the default GITHUB_TOKEN

#### For AWS Bedrock:

1. An AWS account with Amazon Bedrock enabled
2. GitHub OIDC Identity Provider configured in AWS
3. An IAM role with Bedrock permissions
4. A GitHub App (recommended) or use the default GITHUB_TOKEN

<Steps>
  <Step title="Create a custom GitHub App (Recommended for 3P Providers)">
    For best control and security when using 3P providers like Vertex AI or Bedrock, we recommend creating your own GitHub App:

    1. Go to [https://github.com/settings/apps/new](https://github.com/settings/apps/new)
    2. Fill in the basic information:
       * **GitHub App name**: Choose a unique name (e.g., "YourOrg Claude Assistant")
       * **Homepage URL**: Your organization's website or the repository URL
    3. Configure the app settings:
       * **Webhooks**: Uncheck "Active" (not needed for this integration)
    4. Set the required permissions:
       * **Repository permissions**:
         * Contents: Read & Write
         * Issues: Read & Write
         * Pull requests: Read & Write
    5. Click "Create GitHub App"
    6. After creation, click "Generate a private key" and save the downloaded `.pem` file
    7. Note your App ID from the app settings page
    8. Install the app to your repository:
       * From your app's settings page, click "Install App" in the left sidebar
       * Select your account or organization
       * Choose "Only select repositories" and select the specific repository
       * Click "Install"
    9. Add the private key as a secret to your repository:
       * Go to your repository's Settings → Secrets and variables → Actions
       * Create a new secret named `APP_PRIVATE_KEY` with the contents of the `.pem` file
    10. Add the App ID as a secret:

    * Create a new secret named `APP_ID` with your GitHub App's ID

    <Note>
      This app will be used with the [actions/create-github-app-token](https://github.com/actions/create-github-app-token) action to generate authentication tokens in your workflows.
    </Note>

    **Alternative for Anthropic API or if you don't want to setup your own Github app**: Use the official Anthropic app:

    1. Install from: [https://github.com/apps/claude](https://github.com/apps/claude)
    2. No additional configuration needed for authentication

  </Step>

  <Step title="Configure cloud provider authentication">
    Choose your cloud provider and set up secure authentication:

    <AccordionGroup>
      <Accordion title="AWS Bedrock">
        **Configure AWS to allow GitHub Actions to authenticate securely without storing credentials.**

        > **Security Note**: Use repository-specific configurations and grant only the minimum required permissions.

        **Required Setup**:

        1. **Enable Amazon Bedrock**:
           * Request access to Claude models in Amazon Bedrock
           * For cross-region models, request access in all required regions

        2. **Set up GitHub OIDC Identity Provider**:
           * Provider URL: `https://token.actions.githubusercontent.com`
           * Audience: `sts.amazonaws.com`

        3. **Create IAM Role for GitHub Actions**:
           * Trusted entity type: Web identity
           * Identity provider: `token.actions.githubusercontent.com`
           * Permissions: `AmazonBedrockFullAccess` policy
           * Configure trust policy for your specific repository

        **Required Values**:

        After setup, you'll need:

        * **AWS\_ROLE\_TO\_ASSUME**: The ARN of the IAM role you created

        <Tip>
          OIDC is more secure than using static AWS access keys because credentials are temporary and automatically rotated.
        </Tip>

        See [AWS documentation](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_create_oidc.html) for detailed OIDC setup instructions.
      </Accordion>

      <Accordion title="Google Vertex AI">
        **Configure Google Cloud to allow GitHub Actions to authenticate securely without storing credentials.**

        > **Security Note**: Use repository-specific configurations and grant only the minimum required permissions.

        **Required Setup**:

        1. **Enable APIs** in your Google Cloud project:
           * IAM Credentials API
           * Security Token Service (STS) API
           * Vertex AI API

        2. **Create Workload Identity Federation resources**:
           * Create a Workload Identity Pool
           * Add a GitHub OIDC provider with:
             * Issuer: `https://token.actions.githubusercontent.com`
             * Attribute mappings for repository and owner
             * **Security recommendation**: Use repository-specific attribute conditions

        3. **Create a Service Account**:
           * Grant only `Vertex AI User` role
           * **Security recommendation**: Create a dedicated service account per repository

        4. **Configure IAM bindings**:
           * Allow the Workload Identity Pool to impersonate the service account
           * **Security recommendation**: Use repository-specific principal sets

        **Required Values**:

        After setup, you'll need:

        * **GCP\_WORKLOAD\_IDENTITY\_PROVIDER**: The full provider resource name
        * **GCP\_SERVICE\_ACCOUNT**: The service account email address

        <Tip>
          Workload Identity Federation eliminates the need for downloadable service account keys, improving security.
        </Tip>

        For detailed setup instructions, consult the [Google Cloud Workload Identity Federation documentation](https://cloud.google.com/iam/docs/workload-identity-federation).
      </Accordion>
    </AccordionGroup>

  </Step>

  <Step title="Add Required Secrets">
    Add the following secrets to your repository (Settings → Secrets and variables → Actions):

    #### For Anthropic API (Direct):

    1. **For API Authentication**:
       * `ANTHROPIC_API_KEY`: Your Anthropic API key from [console.anthropic.com](https://console.anthropic.com)

    2. **For GitHub App (if using your own app)**:
       * `APP_ID`: Your GitHub App's ID
       * `APP_PRIVATE_KEY`: The private key (.pem) content

    #### For Google Cloud Vertex AI

    1. **For GCP Authentication**:
       * `GCP_WORKLOAD_IDENTITY_PROVIDER`
       * `GCP_SERVICE_ACCOUNT`

    2. **For GitHub App (if using your own app)**:
       * `APP_ID`: Your GitHub App's ID
       * `APP_PRIVATE_KEY`: The private key (.pem) content

    #### For AWS Bedrock

    1. **For AWS Authentication**:
       * `AWS_ROLE_TO_ASSUME`

    2. **For GitHub App (if using your own app)**:
       * `APP_ID`: Your GitHub App's ID
       * `APP_PRIVATE_KEY`: The private key (.pem) content

  </Step>

  <Step title="Create workflow files">
    Create GitHub Actions workflow files that integrate with your cloud provider. The examples below show complete configurations for both AWS Bedrock and Google Vertex AI:

    <AccordionGroup>
      <Accordion title="AWS Bedrock workflow">
        **Prerequisites:**

        * AWS Bedrock access enabled with Claude model permissions
        * GitHub configured as an OIDC identity provider in AWS
        * IAM role with Bedrock permissions that trusts GitHub Actions

        **Required GitHub secrets:**

        | Secret Name          | Description                                       |
        | -------------------- | ------------------------------------------------- |
        | `AWS_ROLE_TO_ASSUME` | ARN of the IAM role for Bedrock access            |
        | `APP_ID`             | Your GitHub App ID (from app settings)            |
        | `APP_PRIVATE_KEY`    | The private key you generated for your GitHub App |

        ```yaml
        name: Claude PR Action

        permissions:
          contents: write
          pull-requests: write
          issues: write
          id-token: write

        on:
          issue_comment:
            types: [created]
          pull_request_review_comment:
            types: [created]
          issues:
            types: [opened, assigned]

        jobs:
          claude-pr:
            if: |
              (github.event_name == 'issue_comment' && contains(github.event.comment.body, '@claude')) ||
              (github.event_name == 'pull_request_review_comment' && contains(github.event.comment.body, '@claude')) ||
              (github.event_name == 'issues' && contains(github.event.issue.body, '@claude'))
            runs-on: ubuntu-latest
            env:
              AWS_REGION: us-west-2
            steps:
              - name: Checkout repository
                uses: actions/checkout@v4

              - name: Generate GitHub App token
                id: app-token
                uses: actions/create-github-app-token@v2
                with:
                  app-id: ${{ secrets.APP_ID }}
                  private-key: ${{ secrets.APP_PRIVATE_KEY }}

              - name: Configure AWS Credentials (OIDC)
                uses: aws-actions/configure-aws-credentials@v4
                with:
                  role-to-assume: ${{ secrets.AWS_ROLE_TO_ASSUME }}
                  aws-region: us-west-2

              - uses: ./.github/actions/claude-pr-action
                with:
                  trigger_phrase: "@claude"
                  timeout_minutes: "60"
                  github_token: ${{ steps.app-token.outputs.token }}
                  use_bedrock: "true"
                  model: "us.anthropic.claude-3-7-sonnet-20250219-v1:0"
        ```

        <Tip>
          The model ID format for Bedrock includes the region prefix (e.g., `us.anthropic.claude...`) and version suffix.
        </Tip>
      </Accordion>

      <Accordion title="Google Vertex AI workflow">
        **Prerequisites:**

        * Vertex AI API enabled in your GCP project
        * Workload Identity Federation configured for GitHub
        * Service account with Vertex AI permissions

        **Required GitHub secrets:**

        | Secret Name                      | Description                                       |
        | -------------------------------- | ------------------------------------------------- |
        | `GCP_WORKLOAD_IDENTITY_PROVIDER` | Workload identity provider resource name          |
        | `GCP_SERVICE_ACCOUNT`            | Service account email with Vertex AI access       |
        | `APP_ID`                         | Your GitHub App ID (from app settings)            |
        | `APP_PRIVATE_KEY`                | The private key you generated for your GitHub App |

        ```yaml
        name: Claude PR Action

        permissions:
          contents: write
          pull-requests: write
          issues: write
          id-token: write

        on:
          issue_comment:
            types: [created]
          pull_request_review_comment:
            types: [created]
          issues:
            types: [opened, assigned]

        jobs:
          claude-pr:
            if: |
              (github.event_name == 'issue_comment' && contains(github.event.comment.body, '@claude')) ||
              (github.event_name == 'pull_request_review_comment' && contains(github.event.comment.body, '@claude')) ||
              (github.event_name == 'issues' && contains(github.event.issue.body, '@claude'))
            runs-on: ubuntu-latest
            steps:
              - name: Checkout repository
                uses: actions/checkout@v4

              - name: Generate GitHub App token
                id: app-token
                uses: actions/create-github-app-token@v2
                with:
                  app-id: ${{ secrets.APP_ID }}
                  private-key: ${{ secrets.APP_PRIVATE_KEY }}

              - name: Authenticate to Google Cloud
                id: auth
                uses: google-github-actions/auth@v2
                with:
                  workload_identity_provider: ${{ secrets.GCP_WORKLOAD_IDENTITY_PROVIDER }}
                  service_account: ${{ secrets.GCP_SERVICE_ACCOUNT }}

              - uses: ./.github/actions/claude-pr-action
                with:
                  trigger_phrase: "@claude"
                  timeout_minutes: "60"
                  github_token: ${{ steps.app-token.outputs.token }}
                  use_vertex: "true"
                  model: "claude-3-7-sonnet@20250219"
                env:
                  ANTHROPIC_VERTEX_PROJECT_ID: ${{ steps.auth.outputs.project_id }}
                  CLOUD_ML_REGION: us-east5
                  VERTEX_REGION_CLAUDE_3_7_SONNET: us-east5
        ```

        <Tip>
          The project ID is automatically retrieved from the Google Cloud authentication step, so you don't need to hardcode it.
        </Tip>
      </Accordion>
    </AccordionGroup>

  </Step>
</Steps>

## Troubleshooting

### Claude not responding to @claude commands

Verify the GitHub App is installed correctly, check that workflows are enabled, ensure API key is set in repository secrets, and confirm the comment contains `@claude` (not `/claude`).

### CI not running on Claude's commits

Ensure you're using the GitHub App or custom app (not Actions user), check workflow triggers include the necessary events, and verify app permissions include CI triggers.

### Authentication errors

Confirm API key is valid and has sufficient permissions. For Bedrock/Vertex, check credentials configuration and ensure secrets are named correctly in workflows.

## Advanced configuration

### Action parameters

The Claude Code Action supports these key parameters:

| Parameter           | Description                    | Required |
| ------------------- | ------------------------------ | -------- |
| `prompt`            | The prompt to send to Claude   | Yes\*    |
| `prompt_file`       | Path to file containing prompt | Yes\*    |
| `anthropic_api_key` | Anthropic API key              | Yes\*\*  |
| `max_turns`         | Maximum conversation turns     | No       |
| `timeout_minutes`   | Execution timeout              | No       |

\*Either `prompt` or `prompt_file` required\
\*\*Required for direct Anthropic API, not for Bedrock/Vertex

### Alternative integration methods

While the `/install-github-app` command is the recommended approach, you can also:

- **Custom GitHub App**: For organizations needing branded usernames or custom authentication flows. Create your own GitHub App with required permissions (contents, issues, pull requests) and use the actions/create-github-app-token action to generate tokens in your workflows.
- **Manual GitHub Actions**: Direct workflow configuration for maximum flexibility
- **MCP Configuration**: Dynamic loading of Model Context Protocol servers

See the [Claude Code Action repository](https://github.com/anthropics/claude-code-action) for detailed documentation.

### Customizing Claude's behavior

You can configure Claude's behavior in two ways:

1. **CLAUDE.md**: Define coding standards, review criteria, and project-specific rules in a `CLAUDE.md` file at the root of your repository. Claude will follow these guidelines when creating PRs and responding to requests. Check out our [Memory documentation](/en/docs/claude-code/memory) for more details.
2. **Custom prompts**: Use the `prompt` parameter in the workflow file to provide workflow-specific instructions. This allows you to customize Claude's behavior for different workflows or tasks.

Claude will follow these guidelines when creating PRs and responding to requests.
