# Linux Environment Variables

In Linux, environment variables are dynamic values that affect the behavior of processes and the shell. They are essential for configuring system settings, defining user preferences, and managing application behavior. Here’s a comprehensive guide to understanding and managing environment variables in Linux.

Author

Benedict Thekkel

## 🔍 What Are Environment Variables?

Environment variables are key-value pairs that provide information about the system environment to processes. They are inherited by child processes and can influence the execution of commands and applications

**Common environment variables include:**

- `PATH`:Specifies directories to search for executable files
- `HOME`:Indicates the current user’s home directory
- `USER`:Stores the name of the current user
- `SHELL`:Defines the path to the current user’s shell
- `LANG`:Sets the system’s locale and language settings

------------------------------------------------------------------------

## 🧰 Managing Environment Variables

### 1. **Listing Environment Variables**

To display all environment variable:

``` bash
printenv
``

Or, to display a specific variabl:

```bash
echo $VARIABLE_NAME
```

For example, to check the `PATH` variable:

``` bash
echo $PATH
```

------------------------------------------------------------------------

### 2. **Setting Environment Variables Temporarily**

To set an environment variable for the current session:

``` bash
export VARIABLE_NAME="value"
```

For example:

``` bash
export JAVA_HOME="/usr/lib/jvm/java-11-openjdk"
```

This variable will be available until the session end.

### 3. **Setting Environment Variables Permanently**

To make an environment variable persistent across sessions, add it to your shell’s initialization file:

For Bash:

``` bash
  echo 'export VARIABLE_NAME="value"' >> ~/.bashrc
  source ~/.bashrc
```

For Zsh:

``` bash
  echo 'export VARIABLE_NAME="value"' >> ~/.zshrc
  source ~/.zshrc
```

For system-wide variables, add them to `/etc/environment` or create a script in `/etc/profile.d/`:

``` bash
echo 'export VARIABLE_NAME="value"' | sudo tee /etc/profile.d/custom_env.sh
sudo chmod +x /etc/profile.d/custom_env.sh
```

------------------------------------------------------------------------

## 🧠 Best Practices

- \*\*Use uppercase names\*: By convention, environment variable names are uppercase to distinguish them from shell variables.

- \*\*Be cautious with `PATH`\*: When modifying `PATH`, append directories rather than replacing its value to avoid overwriting existing paths.

- \*\*Secure sensitive data\*: Avoid storing sensitive information like passwords directly in environment variables. Use secure methods for handling such data.

- \*\*Document changes\*: Keep track of modifications to environment variables, especially system-wide changes, to maintain system integrity.

------------------------------------------------------------------------

## 🛠 Troubleshooting

- **Variable not found**: Ensure the variable is defined in the correct initialization file and that the file is sourced.

- **Changes not reflected**: After modifying initialization files, run `source ~/.bashrc` (or the appropriate file) to apply chances.

- **Conflicting variables**: Check for conflicting definitions in multiple files and resolve them to prevent unexpected behavior.

------------------------------------------------------------------------

## 📚 Additional Resources

- [How to List, Set and Manage Linux Environment Variables](https://www.cherryservers.com/blog/how-to-set-list-and-manage-linux-environment-variables)

- [How to Set Environment Variables in Linux - freeCodeCamp](https://www.freecodecamp.org/news/how-to-set-an-environment-variable-in-linux/)

- [Managing Environment Variables in Linux - Baeldung](https://www.baeldung.com/linux/environment-variables)

------------------------------------------------------------------------

Back to top
