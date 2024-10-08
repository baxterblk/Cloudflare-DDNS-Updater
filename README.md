# Cloudflare DDNS Updater

This project provides a Dynamic DNS (DDNS) updater for Cloudflare, allowing you to automatically update your domain's DNS records when your IP address changes. It's particularly useful for home servers or any setup where you don't have a static IP address.

## Features

- Automatic updating of Cloudflare DNS records
- Web interface for easy management
- Docker support for easy deployment
- Multi-domain support

<img width="934" alt="cloudflare_ddns_updater" src="https://github.com/user-attachments/assets/f6102339-5a40-4b24-b52c-0b7775f8aad7">

## Prerequisites

- Python 3.7+
- Docker (optional, for containerized deployment)
- Cloudflare account with API access

## Installation

### Option 1: Direct Installation

1. Clone the repository:
   ```
   git clone https://github.com/baxterblk/Cloudflare-DDNS-Updater.git
   cd Cloudflare-DDNS-Updater
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Set up your environment variables (see Configuration section below)

4. Run the application:
   ```
   python app.py
   ```

### Option 2: Docker Installation

1. Clone the repository:
   ```
   git clone https://github.com/baxterblk/Cloudflare-DDNS-Updater.git
   cd Cloudflare-DDNS-Updater
   ```

2. Build and run the Docker container:
   ```
   docker-compose up -d
   ```

## Configuration

Create a `.env` file in the root directory with the following content:

```
CLOUDFLARE_API_TOKEN=your_cloudflare_api_token
UPDATE_INTERVAL=300  # Update interval in seconds
```

Replace `your_cloudflare_api_token` with your actual Cloudflare API token.

## Usage

1. Access the web interface by navigating to `http://localhost:5000` in your web browser.
2. Add your domains and the specific DNS records you want to keep updated.
3. The application will automatically check for IP changes and update the specified records at the set interval.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to Cloudflare for providing a robust API for DNS management.
- This project was inspired by the need for a simple, self-hosted DDNS solution for Cloudflare users.
