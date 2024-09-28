#!/bin/bash

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check if ssh-keygen is available
if ! command_exists ssh-keygen; then
    echo "ssh-keygen is not installed. Please install openssh-client and try again."
    exit 1
fi

# Generate SSH key
echo "Generating a new SSH key..."
read -p "Enter your email address: " email
ssh-keygen -t rsa -b 4096 -C "$email"

# Start the ssh-agent in the background
eval "$(ssh-agent -s)"

# Add your SSH key to the ssh-agent
ssh-add ~/.ssh/id_rsa

# Display the public key
echo "Here's your public SSH key:"
cat ~/.ssh/id_rsa.pub

echo "
Instructions:
1. Copy the above public key (starts with 'ssh-rsa' and ends with your email).
2. Go to your Git account settings (e.g., GitHub, GitLab).
3. Find the 'SSH and GPG keys' section.
4. Click 'New SSH key' or 'Add SSH key'.
5. Paste your key into the 'Key' field.
6. Give your key a descriptive title.
7. Click 'Add SSH key' to save.

After adding the key, test your connection:
ssh -T git@github.com  # For GitHub
ssh -T git@gitlab.com  # For GitLab

If successful, you should see a welcome message.
"

# Offer to test the connection
read -p "Would you like to test the connection to GitHub now? (y/n) " test_connection
if [ "$test_connection" = "y" ]; then
    ssh -T git@github.com
fi

echo "SSH key setup complete!"