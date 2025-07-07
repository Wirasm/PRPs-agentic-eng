# CLAUDE.md

This file provides comprehensive guidance for working with Rust applications.

## Core Development Philosophy

### Safety First
Rust's ownership system prevents entire classes of bugs. Embrace the borrow checker and use it to write safer code. When the compiler complains, it's usually catching a real bug.

### Zero-Cost Abstractions
Use Rust's powerful type system and abstractions without worrying about runtime overhead. The compiler optimizes away most abstractions at compile time.

### Concurrency Without Fear
Rust's ownership system makes it safe to write concurrent code. Use channels, async/await, and other concurrency primitives confidently.

## Core Principles

### Ownership & Borrowing
- **Move by Default**: Values are moved unless explicitly borrowed
- **Borrow When Possible**: Use references (&T) instead of owned values when you don't need ownership
- **Mutable XOR Aliasing**: Either have one mutable reference OR many immutable references, never both

### Error Handling
- **Use Result<T, E>**: Never panic in library code, always return Result
- **Propagate with ?**: Use the ? operator to propagate errors up the call stack
- **Custom Error Types**: Create domain-specific error types for better error handling

### Performance
- **Profile First**: Don't optimize without measuring
- **Avoid Unnecessary Clones**: Use references and borrowing to avoid expensive copies
- **Iterator Chains**: Use iterator adapters for efficient data processing

## 🤖 AI Assistant Guidelines

### Context Awareness
- When implementing features, always check existing patterns first
- Use existing error types and patterns in the codebase
- Check for similar functionality in other modules
- Follow existing naming conventions and module organization

### Common Pitfalls to Avoid
- Using unwrap() or expect() in production code
- Ignoring compiler warnings
- Creating unnecessary String allocations
- Fighting the borrow checker instead of understanding it

### Workflow Patterns
- Write tests BEFORE implementation (TDD)
- Use cargo clippy for linting
- Run cargo fmt for consistent formatting
- Use cargo check for fast compilation feedback

## 🦀 Rust Best Practices

### Project Structure

```
src/
├── main.rs           # Binary entry point
├── lib.rs            # Library root
├── config/           # Configuration handling
├── error.rs          # Custom error types
├── models/           # Data structures
├── services/         # Business logic
├── handlers/         # HTTP/API handlers
└── utils/            # Utility functions
```

### Cargo.toml Configuration

```toml
[package]
name = "my-rust-app"
version = "0.1.0"
edition = "2021"
rust-version = "1.70"

[dependencies]
tokio = { version = "1.0", features = ["full"] }
serde = { version = "1.0", features = ["derive"] }
anyhow = "1.0"
thiserror = "1.0"

[dev-dependencies]
tokio-test = "0.4"
criterion = "0.5"
```

### Error Handling Patterns

```rust
// Custom error type with thiserror
#[derive(Debug, thiserror::Error)]
pub enum AppError {
    #[error("Database error: {0}")]
    Database(#[from] sqlx::Error),
    
    #[error("Validation error: {message}")]
    Validation { message: String },
    
    #[error("Not found: {resource}")]
    NotFound { resource: String },
}

// Result type alias
pub type Result<T> = std::result::Result<T, AppError>;

// Function with proper error handling
pub async fn get_user(id: i64) -> Result<User> {
    let user = sqlx::query_as!(User, "SELECT * FROM users WHERE id = ?", id)
        .fetch_optional(&pool)
        .await?
        .ok_or_else(|| AppError::NotFound { 
            resource: format!("User with id {}", id) 
        })?;
    
    Ok(user)
}
```

### Async Patterns

```rust
// Async function with proper error handling
pub async fn fetch_data(url: &str) -> Result<String> {
    let response = reqwest::get(url)
        .await?
        .error_for_status()?;
    
    let body = response.text().await?;
    Ok(body)
}

// Concurrent processing
pub async fn process_items(items: Vec<Item>) -> Vec<Result<ProcessedItem>> {
    use futures::stream::{self, StreamExt};
    
    stream::iter(items)
        .map(|item| async move { process_item(item).await })
        .buffer_unordered(10)  // Process up to 10 items concurrently
        .collect()
        .await
}
```

### Testing Patterns

```rust
#[cfg(test)]
mod tests {
    use super::*;
    use tokio_test;
    
    #[tokio::test]
    async fn test_user_creation() {
        let user = User::new("test@example.com", "Test User");
        assert_eq!(user.email, "test@example.com");
        assert_eq!(user.name, "Test User");
    }
    
    #[tokio::test]
    async fn test_error_handling() {
        let result = get_user(-1).await;
        assert!(result.is_err());
        
        match result {
            Err(AppError::NotFound { resource }) => {
                assert!(resource.contains("User with id"));
            }
            _ => panic!("Expected NotFound error"),
        }
    }
}
```

## 🛠️ Development Tools

### Essential Cargo Commands

```bash
# Development
cargo check                    # Fast compilation check
cargo clippy                   # Linting
cargo fmt                      # Code formatting
cargo test                     # Run tests
cargo bench                    # Run benchmarks

# Build
cargo build                    # Debug build
cargo build --release          # Optimized build

# Documentation
cargo doc --open               # Generate and open docs

# Security
cargo audit                    # Security vulnerability scan
```

### VS Code Extensions
- rust-analyzer (language server)
- CodeLLDB (debugger)
- crates (dependency management)

## 🔒 Security & Safety

### Memory Safety
- Rust prevents buffer overflows, use-after-free, and double-free bugs
- The borrow checker ensures memory safety at compile time
- Use smart pointers (Box, Rc, Arc) when ownership is complex

### Unsafe Code Guidelines
- Avoid unsafe code unless absolutely necessary
- Document why unsafe is needed
- Minimize the unsafe block scope
- Provide safe abstractions over unsafe code

### Input Validation
```rust
use serde::{Deserialize, Serialize};
use validator::{Validate, ValidationError};

#[derive(Debug, Deserialize, Validate)]
pub struct CreateUserRequest {
    #[validate(email)]
    pub email: String,
    
    #[validate(length(min = 2, max = 50))]
    pub name: String,
    
    #[validate(length(min = 8))]
    pub password: String,
}

pub fn validate_user_input(input: &CreateUserRequest) -> Result<()> {
    input.validate()
        .map_err(|e| AppError::Validation { 
            message: format!("{}", e) 
        })?;
    Ok(())
}
```

## 📊 Performance Guidelines

### Memory Management
- Use Vec::with_capacity() when you know the size
- Prefer &str over String when you don't need ownership
- Use Cow<str> for potentially borrowed strings
- Pool expensive resources like database connections

### Async Performance
```rust
// Good: Use buffered streams for concurrent processing
use futures::stream::{self, StreamExt};

let results: Vec<_> = stream::iter(items)
    .map(|item| process_item(item))
    .buffer_unordered(10)
    .collect()
    .await;

// Good: Use join! for concurrent independent operations
let (result1, result2) = tokio::join!(
    fetch_data(url1),
    fetch_data(url2)
);
```

## ⚠️ Critical Guidelines

1. **Never use unwrap() in production** - Always handle errors properly
2. **Use the type system** - Let the compiler catch bugs for you
3. **Follow ownership rules** - Don't fight the borrow checker
4. **Write tests first** - TDD works especially well with Rust
5. **Use clippy** - It catches many common mistakes and anti-patterns
6. **Profile before optimizing** - Don't guess where the bottlenecks are
7. **Handle errors explicitly** - Use Result<T, E> and ? operator
8. **Use iterators** - They're zero-cost and often more readable
9. **Embrace immutability** - Make things mut only when necessary
10. **Document unsafe code** - Explain why it's needed and how it's safe

## 📋 Pre-commit Checklist

- [ ] All tests pass: `cargo test`
- [ ] No clippy warnings: `cargo clippy -- -D warnings`
- [ ] Code is formatted: `cargo fmt`
- [ ] Documentation builds: `cargo doc`
- [ ] No security vulnerabilities: `cargo audit`
- [ ] Benchmarks don't regress (if applicable)
- [ ] Error handling is comprehensive
- [ ] No unwrap() or expect() in production code

## 🔧 Useful Commands

```bash
# Development workflow
cargo watch -x check           # Auto-run check on file changes
cargo watch -x test            # Auto-run tests on file changes
cargo expand                   # Show macro expansions

# Performance analysis
cargo flamegraph               # Generate flame graphs
cargo asm                      # Show generated assembly
cargo llvm-lines               # Count LLVM IR lines

# Cross-compilation
cargo build --target x86_64-unknown-linux-musl

# Release preparation
cargo package                 # Prepare for publishing
cargo publish --dry-run       # Test publishing
```

---

*Keep this guide updated as patterns evolve. Safety and performance through Rust's type system, always.*