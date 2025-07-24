#!/bin/bash

# PRP Framework Setup Script
# Automates the manual steps from README.md Option 1 to integrate PRP Framework into existing projects

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to show usage
show_usage() {
    echo "Usage: $0 <source_prp_path> <target_project_path>"
    echo ""
    echo "Arguments:"
    echo "  source_prp_path    Path to the PRPs-agentic-eng repository"
    echo "  target_project_path Path to your existing project where PRP Framework will be installed"
    echo ""
    echo "Example:"
    echo "  $0 /path/to/PRPs-agentic-eng /path/to/my-project"
    echo ""
    echo "This script automates the manual steps from README.md Option 1:"
    echo "  1. Copies .claude/commands to target project"
    echo "  2. Copies PRP templates, scripts, and README"
    echo "  3. Copies AI documentation (optional)"
}

# Function to validate paths
validate_path() {
    local path="$1"
    local type="$2"
    
    if [[ ! -d "$path" ]]; then
        print_error "$type directory does not exist: $path"
        return 1
    fi
    
    if [[ ! -r "$path" ]]; then
        print_error "$type directory is not readable: $path"
        return 1
    fi
    
    return 0
}

# Function to validate source PRP repository
validate_source() {
    local source_path="$1"
    
    print_status "Validating source PRP repository..."
    
    # Check if it's the correct repository structure
    if [[ ! -d "$source_path/.claude/commands" ]]; then
        print_error "Source does not appear to be a valid PRPs-agentic-eng repository"
        print_error "Missing: $source_path/.claude/commands"
        return 1
    fi
    
    if [[ ! -d "$source_path/PRPs/templates" ]]; then
        print_error "Source does not appear to be a valid PRPs-agentic-eng repository"
        print_error "Missing: $source_path/PRPs/templates"
        return 1
    fi
    
    if [[ ! -d "$source_path/PRPs/scripts" ]]; then
        print_error "Source does not appear to be a valid PRPs-agentic-eng repository"
        print_error "Missing: $source_path/PRPs/scripts"
        return 1
    fi
    
    print_success "Source repository validation passed"
    return 0
}

# Function to create directory if it doesn't exist
ensure_directory() {
    local dir="$1"
    
    if [[ ! -d "$dir" ]]; then
        print_status "Creating directory: $dir"
        mkdir -p "$dir"
        if [[ $? -eq 0 ]]; then
            print_success "Directory created: $dir"
        else
            print_error "Failed to create directory: $dir"
            return 1
        fi
    else
        print_status "Directory already exists: $dir"
    fi
    
    return 0
}

# Function to copy with backup if destination exists
safe_copy() {
    local source="$1"
    local destination="$2"
    local description="$3"
    
    print_status "Copying $description..."
    print_status "From: $source"
    print_status "To: $destination"
    
    # Check if destination exists and create backup
    if [[ -e "$destination" ]]; then
        local backup="${destination}.backup.$(date +%Y%m%d_%H%M%S)"
        print_warning "Destination exists, creating backup: $backup"
        cp -r "$destination" "$backup"
        if [[ $? -eq 0 ]]; then
            print_success "Backup created: $backup"
        else
            print_error "Failed to create backup: $backup"
            return 1
        fi
    fi
    
    # Perform the copy
    cp -r "$source" "$destination"
    if [[ $? -eq 0 ]]; then
        print_success "Successfully copied $description"
    else
        print_error "Failed to copy $description"
        return 1
    fi
    
    return 0
}

# Main function
main() {
    # Check arguments
    if [[ $# -ne 2 ]]; then
        show_usage
        exit 1
    fi
    
    local source_path="$1"
    local target_path="$2"
    
    # Convert to absolute paths
    source_path=$(realpath "$source_path" 2>/dev/null) || source_path="$1"
    target_path=$(realpath "$target_path" 2>/dev/null) || target_path="$2"
    
    print_status "PRP Framework Setup Script"
    print_status "=========================="
    print_status "Source: $source_path"
    print_status "Target: $target_path"
    echo ""
    
    # Validate inputs
    if ! validate_path "$source_path" "Source"; then
        exit 1
    fi
    
    if ! validate_path "$target_path" "Target"; then
        exit 1
    fi
    
    if ! validate_source "$source_path"; then
        exit 1
    fi
    
    # Ensure target project is writable
    if [[ ! -w "$target_path" ]]; then
        print_error "Target directory is not writable: $target_path"
        exit 1
    fi
    
    echo ""
    print_status "Starting PRP Framework installation..."
    echo ""
    
    # Step 1: Copy Claude commands
    print_status "Step 1: Copying Claude commands"
    print_status "==============================="
    
    ensure_directory "$target_path/.claude" || exit 1
    safe_copy "$source_path/.claude/commands" "$target_path/.claude/commands" "Claude commands" || exit 1
    
    echo ""
    
    # Step 2: Copy PRP templates and runner
    print_status "Step 2: Copying PRP templates and scripts"
    print_status "========================================="
    
    ensure_directory "$target_path/PRPs" || exit 1
    safe_copy "$source_path/PRPs/templates" "$target_path/PRPs/templates" "PRP templates" || exit 1
    safe_copy "$source_path/PRPs/scripts" "$target_path/PRPs/scripts" "PRP scripts" || exit 1
    safe_copy "$source_path/PRPs/README.md" "$target_path/PRPs/README.md" "PRP README" || exit 1
    
    echo ""
    
    # Step 3: Copy AI documentation (optional)
    print_status "Step 3: Copying AI documentation (optional)"
    print_status "==========================================="
    
    if [[ -d "$source_path/PRPs/ai_docs" ]]; then
        echo -n "Copy AI documentation? This is optional but recommended. [Y/n]: "
        read -r response
        if [[ "$response" =~ ^[Nn]$ ]]; then
            print_warning "Skipping AI documentation copy"
        else
            safe_copy "$source_path/PRPs/ai_docs" "$target_path/PRPs/ai_docs" "AI documentation" || exit 1
        fi
    else
        print_warning "AI documentation not found in source repository"
    fi
    
    echo ""
    
    # Step 4: Copy settings template if it doesn't exist
    print_status "Step 4: Setting up Claude configuration"
    print_status "======================================"
    
    if [[ -f "$source_path/.claude/settings.json" ]]; then
        if [[ ! -f "$target_path/.claude/settings.json" ]]; then
            safe_copy "$source_path/.claude/settings.json" "$target_path/.claude/settings.json" "Claude settings" || exit 1
        else
            print_warning "Claude settings already exist in target project"
            print_warning "You may want to merge settings from: $source_path/.claude/settings.json"
        fi
    fi
    
    echo ""
    
    # Final summary
    print_success "================================="
    print_success "PRP Framework Installation Complete!"
    print_success "================================="
    echo ""
    print_status "What was installed:"
    print_status "• Claude commands: $target_path/.claude/commands/"
    print_status "• PRP templates: $target_path/PRPs/templates/"
    print_status "• PRP scripts: $target_path/PRPs/scripts/"
    print_status "• PRP README: $target_path/PRPs/README.md"
    
    if [[ -d "$target_path/PRPs/ai_docs" ]]; then
        print_status "• AI documentation: $target_path/PRPs/ai_docs/"
    fi
    
    if [[ -f "$target_path/.claude/settings.json" ]]; then
        print_status "• Claude settings: $target_path/.claude/settings.json"
    fi
    
    echo ""
    print_status "Next steps:"
    print_status "1. Create a CLAUDE.md file in your project root with project-specific guidelines"
    print_status "2. Open your project in Claude Code to access the new commands"
    print_status "3. Try running: /prp-base-create your-first-feature"
    print_status "4. Review the documentation in PRPs/README.md for detailed usage"
    echo ""
    print_success "Happy coding with the PRP Framework! 🚀"
}

# Run main function with all arguments
main "$@"