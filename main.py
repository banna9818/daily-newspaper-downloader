#!/usr/bin/env python3
"""
Daily Gujarat Samachar Newspaper Downloader
Downloads the daily Gujarat Samachar Rajkot-Saurashtra newspaper,
converts all pages to PDF, and uploads to Telegram channel.

Author: Banna9818
Date: 2026-06-17
"""

import os
import sys
import logging
import asyncio
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional
import re

import requests
from PIL import Image
from io import BytesIO
import pytz

# Try to import playwright for dynamic content
try:
    from playwright.async_api import async_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("Warning: Playwright not available. Will use basic requests.")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('newspaper_download.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class NewspaperDownloader:
    """
    Downloads Gujarat Samachar newspaper from the website.
    Handles dynamic content loading with Playwright if available.
    """

    BASE_URL = "https://sandesh-pages.vercel.app/gujarat-samachar/rajkot-saurashtra"
    TIMEOUT = 30
    MAX_RETRIES = 3

    def __init__(self):
        """Initialize the downloader with timezone settings."""
        self.ist = pytz.timezone('Asia/Kolkata')
        self.today_date = datetime.now(self.ist).strftime('%Y-%m-%d')
        self.pages = []
        self.pdf_filename = f"Gujarat_Samachar_Rajkot_{self.today_date}.pdf"
        logger.info(f"Initialized downloader for date: {self.today_date}")

    def get_today_date(self) -> str:
        """
        Get today's date in Asia/Kolkata timezone.
        
        Returns:
            str: Date in YYYY-MM-DD format
        """
        ist = pytz.timezone('Asia/Kolkata')
        today = datetime.now(ist).strftime('%Y-%m-%d')
        logger.info(f"Today's date in IST: {today}")
        return today

    async def fetch_with_playwright(self) -> Optional[str]:
        """
        Fetch webpage using Playwright to handle dynamic content.
        
        Returns:
            Optional[str]: HTML content of the page or None if failed
        """
        if not PLAYWRIGHT_AVAILABLE:
            logger.warning("Playwright not available, skipping dynamic content loading")
            return None

        try:
            logger.info("Attempting to fetch page with Playwright...")
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                
                url = f"{self.BASE_URL}?date={self.today_date}"
                logger.info(f"Opening URL: {url}")
                
                await page.goto(url, wait_until="networkidle", timeout=self.TIMEOUT * 1000)
                
                # Wait for images to load
                await page.wait_for_selector('img[src*="jpg"]', timeout=10000)
                
                content = await page.content()
                await browser.close()
                
                logger.info("Successfully fetched page with Playwright")
                return content

        except Exception as e:
            logger.error(f"Playwright fetch failed: {e}")
            return None

    def fetch_with_requests(self) -> Optional[str]:
        """
        Fetch webpage using basic requests library.
        
        Returns:
            Optional[str]: HTML content of the page or None if failed
        """
        try:
            logger.info("Attempting to fetch page with requests...")
            url = f"{self.BASE_URL}?date={self.today_date}"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=self.TIMEOUT)
            response.raise_for_status()
            
            logger.info("Successfully fetched page with requests")
            return response.text

        except requests.RequestException as e:
            logger.error(f"Requests fetch failed: {e}")
            return None

    def extract_image_urls(self, html_content: str) -> List[str]:
        """
        Extract all newspaper page image URLs from HTML content.
        
        Args:
            html_content (str): HTML content to parse
            
        Returns:
            List[str]: List of image URLs in order
        """
        try:
            # Pattern to match newspaper page images
            # Looking for img tags with src containing jpg/png
            pattern = r'<img[^>]+src=["\']([^"\']*(?:jpg|png|jpeg)[^"\']*)["\']'
            urls = re.findall(pattern, html_content, re.IGNORECASE)
            
            if not urls:
                logger.warning("No images found with standard pattern, trying alternative...")
                # Alternative pattern
                pattern = r'src=["\']([^"\']*(?:cloudinary|imgur|vercel)[^"\']*)["\']'
                urls = re.findall(pattern, html_content, re.IGNORECASE)
            
            # Filter to keep only valid newspaper page images
            valid_urls = []
            for url in urls:
                if any(domain in url.lower() for domain in ['jpg', 'jpeg', 'png', 'cloudinary', 'imgur']):
                    if 'avatar' not in url.lower() and 'logo' not in url.lower():
                        valid_urls.append(url)
            
            logger.info(f"Extracted {len(valid_urls)} image URLs")
            return valid_urls[:100]  # Safety limit

        except Exception as e:
            logger.error(f"Error extracting image URLs: {e}")
            return []

    def download_image(self, url: str, retry_count: int = 0) -> Optional[Image.Image]:
        """
        Download a single image from URL.
        
        Args:
            url (str): Image URL to download
            retry_count (int): Current retry attempt
            
        Returns:
            Optional[Image.Image]: PIL Image object or None if failed
        """
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Referer': self.BASE_URL
            }
            
            response = requests.get(url, headers=headers, timeout=self.TIMEOUT)
            response.raise_for_status()
            
            # Open image
            img = Image.open(BytesIO(response.content))
            
            # Convert RGBA to RGB if necessary
            if img.mode == 'RGBA':
                rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                rgb_img.paste(img, mask=img.split()[3])
                img = rgb_img
            
            logger.info(f"Successfully downloaded image from {url}")
            return img

        except Exception as e:
            if retry_count < self.MAX_RETRIES:
                logger.warning(f"Retry {retry_count + 1}/{self.MAX_RETRIES} for {url}")
                return self.download_image(url, retry_count + 1)
            logger.error(f"Failed to download image {url}: {e}")
            return None

    async def fetch_and_download_pages(self) -> bool:
        """
        Fetch webpage and download all newspaper pages.
        
        Returns:
            bool: True if at least one page was downloaded, False otherwise
        """
        # Try Playwright first
        html_content = None
        if PLAYWRIGHT_AVAILABLE:
            html_content = await self.fetch_with_playwright()
        
        # Fall back to requests if Playwright failed
        if not html_content:
            html_content = self.fetch_with_requests()
        
        if not html_content:
            logger.error("Failed to fetch webpage with both methods")
            return False
        
        # Extract image URLs
        image_urls = self.extract_image_urls(html_content)
        
        if not image_urls:
            logger.error("No newspaper pages found for the given date")
            return False
        
        logger.info(f"Found {len(image_urls)} pages to download")
        
        # Download images
        for idx, url in enumerate(image_urls, 1):
            logger.info(f"Downloading page {idx}/{len(image_urls)}")
            img = self.download_image(url)
            
            if img:
                self.pages.append(img)
                logger.info(f"Page {idx} downloaded successfully")
            else:
                logger.warning(f"Page {idx} download failed")
        
        if not self.pages:
            logger.error("No pages were successfully downloaded")
            return False
        
        logger.info(f"Successfully downloaded {len(self.pages)} pages")
        return True

    def create_pdf(self) -> bool:
        """
        Merge all downloaded pages into a single PDF.
        
        Returns:
            bool: True if PDF creation successful, False otherwise
        """
        try:
            if not self.pages:
                logger.error("No pages available to create PDF")
                return False
            
            logger.info(f"Creating PDF with {len(self.pages)} pages...")
            
            # Convert all images to RGB
            rgb_pages = []
            for page in self.pages:
                if page.mode != 'RGB':
                    if page.mode == 'RGBA':
                        rgb_img = Image.new('RGB', page.size, (255, 255, 255))
                        rgb_img.paste(page, mask=page.split()[3])
                        rgb_pages.append(rgb_img)
                    else:
                        rgb_pages.append(page.convert('RGB'))
                else:
                    rgb_pages.append(page)
            
            # Create PDF
            if rgb_pages:
                rgb_pages[0].save(
                    self.pdf_filename,
                    save_all=True,
                    append_images=rgb_pages[1:],
                    duration=100,
                    loop=0,
                    quality=55,
                    optimize=False
                )
                
                file_size = os.path.getsize(self.pdf_filename)
                logger.info(f"PDF created successfully: {self.pdf_filename} ({file_size} bytes)")
                return True
            else:
                logger.error("No valid pages to create PDF")
                return False

        except Exception as e:
            logger.error(f"Error creating PDF: {e}")
            return False

    def validate_pdf(self) -> bool:
        """
        Validate that PDF was created and is not empty.
        
        Returns:
            bool: True if PDF is valid, False otherwise
        """
        try:
            if not os.path.exists(self.pdf_filename):
                logger.error(f"PDF file not found: {self.pdf_filename}")
                return False
            
            file_size = os.path.getsize(self.pdf_filename)
            if file_size < 1024:  # Less than 1KB
                logger.error(f"PDF file too small ({file_size} bytes)")
                return False
            
            logger.info(f"PDF validation successful: {file_size} bytes")
            return True

        except Exception as e:
            logger.error(f"Error validating PDF: {e}")
            return False


def send_telegram_message(
    message: str,
    bot_token: str,
    channel_username: str,
    file_path: Optional[str] = None
) -> bool:
    """
    Send message and optional file to Telegram channel.
    
    Args:
        message (str): Message text to send
        bot_token (str): Telegram bot token
        channel_username (str): Channel username or chat ID
        file_path (Optional[str]): Path to file to upload
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        logger.info(f"Sending message to Telegram channel: {channel_username}")
        
        if file_path and os.path.exists(file_path):
            # Send document with caption
            url = f"https://api.telegram.org/bot{bot_token}/sendDocument"
            
            with open(file_path, 'rb') as f:
                files = {'document': f}
                data = {
                    'chat_id': channel_username,
                    'caption': message,
                    'parse_mode': 'HTML'
                }
                
                response = requests.post(url, data=data, files=files, timeout=300)
                response.raise_for_status()
            
            logger.info("Document sent to Telegram successfully")
            return True
        else:
            # Send text message only
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            
            data = {
                'chat_id': channel_username,
                'text': message,
                'parse_mode': 'HTML'
            }
            
            response = requests.post(url, json=data, timeout=30)
            response.raise_for_status()
            
            logger.info("Message sent to Telegram successfully")
            return True

    except Exception as e:
        logger.error(f"Error sending to Telegram: {e}")
        return False


def create_telegram_caption(date_str: str) -> str:
    """
    Create the Telegram message caption with formatted date.
    
    Args:
        date_str (str): Date in YYYY-MM-DD format
        
    Returns:
        str: Formatted Telegram caption
    """
    # Parse date
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    formatted_date = date_obj.strftime('%d-%m-%Y')
    
    caption = f"""📰 ગુજરાત સમાચાર - રાજકોટ સૌરાષ્ટ્ર

📅 {formatted_date}

📖 આજનું સંપૂર્ણ અખબાર PDF સ્વરૂપે

━━━━━━━━━━━━━━

🔥 KHAKHI NI KHUMARI 🔥

━━━━━━━━━━━━━━"""
    
    return caption


async def main():
    """
    Main execution function.
    Orchestrates the entire workflow.
    """
    try:
        # Get credentials from environment
        bot_token = os.getenv('BOT_TOKEN')
        channel_username = os.getenv('CHANNEL_USERNAME')
        
        if not bot_token or not channel_username:
            logger.error("Missing Telegram credentials in environment variables")
            sys.exit(1)
        
        logger.info("=" * 60)
        logger.info("Starting Gujarat Samachar Newspaper Download")
        logger.info("=" * 60)
        
        # Initialize downloader
        downloader = NewspaperDownloader()
        
        # Get today's date
        today_date = downloader.get_today_date()
        
        # Fetch and download pages
        success = await downloader.fetch_and_download_pages()
        
        if not success:
            error_msg = f"Failed to download newspaper for {today_date}"
            logger.error(error_msg)
            send_telegram_message(
                f"❌ ગુજરાત સમાચાર ડાઉનલોડ નિષ્ફળ\n\n⚠️ તારીખ: {today_date}",
                bot_token,
                channel_username
            )
            sys.exit(1)
        
        # Create PDF
        if not downloader.create_pdf():
            logger.error("Failed to create PDF")
            send_telegram_message(
                "❌ PDF બનાવવામાં નિષ્ફળ",
                bot_token,
                channel_username
            )
            sys.exit(1)
        
        # Validate PDF
        if not downloader.validate_pdf():
            logger.error("PDF validation failed")
            send_telegram_message(
                "❌ PDF માન્યતા નિષ્ફળ",
                bot_token,
                channel_username
            )
            sys.exit(1)
        
        # Create Telegram caption
        caption = create_telegram_caption(today_date)
        
        # Send to Telegram
        if send_telegram_message(
            caption,
            bot_token,
            channel_username,
            downloader.pdf_filename
        ):
            logger.info("=" * 60)
            logger.info("Workflow completed successfully!")
            logger.info("=" * 60)
            sys.exit(0)
        else:
            logger.error("Failed to send PDF to Telegram")
            sys.exit(1)

    except KeyboardInterrupt:
        logger.info("Workflow interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    # Run async main function
    asyncio.run(main())
