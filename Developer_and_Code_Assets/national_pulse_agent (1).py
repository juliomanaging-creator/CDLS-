# NATIONAL PULSE AGENT - SOVEREIGN SCRAPING ENGINE
## Enhanced with IP Masking, Rotating Proxies, and Tor Integration

"""
CDLS National Pulse Agent
Monitors real-time EV inventory across strategic clusters with military-grade OPSEC
"""

import asyncio
import random
from datetime import datetime
from typing import Dict, List, Optional
import json
import hashlib

# Core Dependencies
from camoufox.async_api import Camoufox
from playwright.async_api import Browser, Page

# IP Masking & Proxy Rotation
import aiohttp
from stem import Signal
from stem.control import Controller

# Database & Logging
import psycopg2
from psycopg2.extras import execute_values
import logging

# Configuration
import os
from dotenv import load_dotenv

load_dotenv()

# ==========================================
# CONFIGURATION
# ==========================================

# Strategic Clusters (Sacramento, Phoenix, Dallas)
CLUSTERS = {
    "Sacramento": "95825",
    "Phoenix": "85251", 
    "Dallas": "76010",
    "Los Angeles": "90001",
    "San Diego": "92101",
    "San Francisco": "94102",
    "Las Vegas": "89101",
    "Seattle": "98101",
    "Portland": "97201",
    "Denver": "80202"
}

# IP Masking Strategy Selection
IP_STRATEGY = os.getenv("IP_STRATEGY", "rotating_proxies")  # Options: rotating_proxies, tor, vpn, none

# Rotating Proxy Configuration
PROXY_PROVIDERS = {
    "smartproxy": {
        "endpoint": "gate.smartproxy.com:7000",
        "username": os.getenv("SMARTPROXY_USER"),  # Your SmartProxy username
        "password": os.getenv("SMARTPROXY_PASS"),
        "cost": "$75/month for 5GB"
    },
    "brightdata": {
        "endpoint": "brd.superproxy.io:22225",
        "username": os.getenv("BRIGHTDATA_USER"),
        "password": os.getenv("BRIGHTDATA_PASS"),
        "cost": "$500/month for 20GB"
    },
    "oxylabs": {
        "endpoint": "pr.oxylabs.io:7777",
        "username": os.getenv("OXYLABS_USER"),
        "password": os.getenv("OXYLABS_PASS"),
        "cost": "$300/month for 10GB"
    },
    "webshare": {  # Budget option
        "endpoint": "proxy.webshare.io:80",
        "username": os.getenv("WEBSHARE_USER"),
        "password": os.getenv("WEBSHARE_PASS"),
        "cost": "$49/month for 1GB"
    }
}

# Tor Configuration
TOR_PROXY = "socks5://127.0.0.1:9050"
TOR_CONTROL_PORT = 9051
TOR_PASSWORD = os.getenv("TOR_PASSWORD", "")

# Database Configuration
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
    "database": os.getenv("DB_NAME", "cdls_kinetic_mesh"),
    "user": os.getenv("DB_USER", "cdls_admin"),
    "password": os.getenv("DB_PASSWORD", "")
}

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pulse_agent.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ==========================================
# IP MASKING UTILITIES
# ==========================================

class IPMaskingEngine:
    """Handles IP anonymization through multiple strategies"""
    
    def __init__(self, strategy: str = "rotating_proxies"):
        self.strategy = strategy
        self.current_proxy = None
        self.proxy_pool = []
        self.tor_controller = None
        
    async def initialize(self):
        """Initialize selected IP masking strategy"""
        logger.info(f"Initializing IP Masking: {self.strategy}")
        
        if self.strategy == "rotating_proxies":
            await self._init_rotating_proxies()
        elif self.strategy == "tor":
            await self._init_tor()
        elif self.strategy == "vpn":
            await self._init_vpn()
        else:
            logger.warning("No IP masking enabled - using raw connection")
    
    async def _init_rotating_proxies(self):
        """Initialize rotating residential proxy pool"""
        provider = os.getenv("PROXY_PROVIDER", "webshare")  # Default to budget option
        
        if provider not in PROXY_PROVIDERS:
            raise ValueError(f"Unknown proxy provider: {provider}")
        
        config = PROXY_PROVIDERS[provider]
        
        # Build proxy URL
        proxy_url = f"http://{config['username']}:{config['password']}@{config['endpoint']}"
        
        self.proxy_pool = [proxy_url]  # Single proxy for now, can expand to pool
        self.current_proxy = self.proxy_pool[0]
        
        logger.info(f"Initialized {provider} proxy: {config['cost']}")
        logger.info(f"Proxy endpoint: {config['endpoint']}")
    
    async def _init_tor(self):
        """Initialize Tor SOCKS5 proxy"""
        try:
            # Connect to Tor control port
            self.tor_controller = Controller.from_port(port=TOR_CONTROL_PORT)
            self.tor_controller.authenticate(password=TOR_PASSWORD)
            
            logger.info("Connected to Tor network")
            logger.info("Tor circuit established")
            
            # Get current Tor IP
            current_ip = await self._get_tor_ip()
            logger.info(f"Current Tor IP: {current_ip}")
            
        except Exception as e:
            logger.error(f"Tor initialization failed: {e}")
            logger.error("Make sure Tor is installed: brew install tor (Mac) or apt install tor (Linux)")
            raise
    
    async def _init_vpn(self):
        """Initialize VPN connection (placeholder - requires OS-level VPN)"""
        logger.info("VPN strategy selected")
        logger.warning("VPN must be configured at OS level (NordVPN, ExpressVPN, etc.)")
        logger.warning("Pulse Agent will use whatever VPN connection is active")
    
    async def rotate_ip(self):
        """Rotate to a new IP address"""
        if self.strategy == "rotating_proxies":
            # Residential proxies auto-rotate on each request
            logger.info("Proxy will auto-rotate on next request")
            
        elif self.strategy == "tor":
            # Request new Tor circuit
            try:
                self.tor_controller.signal(Signal.NEWNYM)
                await asyncio.sleep(5)  # Wait for new circuit
                
                new_ip = await self._get_tor_ip()
                logger.info(f"Rotated to new Tor IP: {new_ip}")
                
            except Exception as e:
                logger.error(f"Tor rotation failed: {e}")
        
        elif self.strategy == "vpn":
            logger.warning("VPN rotation requires manual reconnection")
    
    async def _get_tor_ip(self) -> str:
        """Get current Tor exit node IP"""
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://api.ipify.org",
                proxy=TOR_PROXY
            ) as response:
                return await response.text()
    
    def get_proxy_config(self) -> Optional[Dict]:
        """Get proxy configuration for browser"""
        if self.strategy == "rotating_proxies":
            # Parse proxy URL
            import urllib.parse
            parsed = urllib.parse.urlparse(self.current_proxy)
            
            return {
                "server": f"{parsed.scheme}://{parsed.hostname}:{parsed.port}",
                "username": parsed.username,
                "password": parsed.password
            }
        
        elif self.strategy == "tor":
            return {
                "server": TOR_PROXY
            }
        
        return None

# ==========================================
# STEALTH BROWSER ENGINE
# ==========================================

class StealthBrowser:
    """Camoufox browser with enhanced stealth and IP masking"""
    
    def __init__(self, ip_engine: IPMaskingEngine):
        self.ip_engine = ip_engine
        self.browser: Optional[Browser] = None
        self.fingerprint_rotation_enabled = True
        
    async def launch(self):
        """Launch stealthy browser with IP masking"""
        proxy_config = self.ip_engine.get_proxy_config()
        
        # Enhanced Camoufox configuration
        camoufox_args = {
            "headless": True,
            "humanize": True,  # Randomizes mouse movements, typing speed
            "screen": {
                "min_width": 1024,
                "max_width": 1920,
                "min_height": 768,
                "max_height": 1080
            },
            "addons": [
                # Could add uBlock Origin, Privacy Badger
            ],
            "fonts": ["Arial", "Helvetica", "Times New Roman"],  # Randomize fonts
            "geoip": True,  # Use proxy's geolocation
            "exclude_addons": ["flash"],  # No Flash fingerprinting
        }
        
        # Add proxy if configured
        if proxy_config:
            camoufox_args["proxy"] = proxy_config
            logger.info(f"Browser launching with proxy: {proxy_config['server']}")
        
        self.browser = await Camoufox(**camoufox_args)
        
        logger.info("Stealth browser launched successfully")
        return self.browser
    
    async def new_page(self) -> Page:
        """Create new page with anti-detection measures"""
        if not self.browser:
            await self.launch()
        
        page = await self.browser.new_page()
        
        # Inject anti-detection scripts
        await self._inject_stealth_scripts(page)
        
        return page
    
    async def _inject_stealth_scripts(self, page: Page):
        """Inject JavaScript to evade detection"""
        
        # Override WebDriver detection
        await page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """)
        
        # Randomize canvas fingerprint
        await page.add_init_script("""
            const originalToDataURL = HTMLCanvasElement.prototype.toDataURL;
            HTMLCanvasElement.prototype.toDataURL = function(type) {
                // Add slight randomization to canvas fingerprint
                const context = this.getContext('2d');
                const imageData = context.getImageData(0, 0, this.width, this.height);
                for (let i = 0; i < imageData.data.length; i += 4) {
                    imageData.data[i] += Math.random() * 0.1 - 0.05;
                }
                context.putImageData(imageData, 0, 0);
                return originalToDataURL.apply(this, arguments);
            };
        """)
        
        # Randomize WebGL fingerprint
        await page.add_init_script("""
            const getParameter = WebGLRenderingContext.prototype.getParameter;
            WebGLRenderingContext.prototype.getParameter = function(parameter) {
                if (parameter === 37445) {
                    return 'Intel Inc.';  // Randomize GPU vendor
                }
                if (parameter === 37446) {
                    return 'Intel Iris OpenGL Engine';  // Randomize GPU renderer
                }
                return getParameter.apply(this, arguments);
            };
        """)
        
        # Spoof navigator properties
        await page.add_init_script("""
            Object.defineProperty(navigator, 'platform', {
                get: () => ['Win32', 'MacIntel', 'Linux x86_64'][Math.floor(Math.random() * 3)]
            });
            
            Object.defineProperty(navigator, 'hardwareConcurrency', {
                get: () => [4, 8, 16][Math.floor(Math.random() * 3)]
            });
        """)
        
        logger.info("Stealth scripts injected")
    
    async def close(self):
        """Close browser gracefully"""
        if self.browser:
            await self.browser.close()
            logger.info("Browser closed")

# ==========================================
# NATIONAL PULSE SCANNER
# ==========================================

async def pulse_scan(
    zip_code: str, 
    cluster_name: str,
    stealth_browser: StealthBrowser,
    ip_engine: IPMaskingEngine
) -> Dict:
    """
    Scrapes real-time EV inventory for a specific cluster with IP rotation
    """
    logger.info(f"Scanning {cluster_name} ({zip_code})")
    
    # Rotate IP before each cluster (reduces detection risk)
    await ip_engine.rotate_ip()
    
    page = await stealth_browser.new_page()
    
    try:
        url = f"https://www.cars.com/shopping/results/?zip={zip_code}&fuel_slugs[]=electric"
        
        logger.info(f"Navigating to: {url}")
        
        # Navigate with realistic timing
        await page.goto(url, wait_until="networkidle", timeout=60000)
        
        # Simulate human behavior
        await asyncio.sleep(random.uniform(2, 5))  # Random delay
        await page.mouse.move(
            random.randint(100, 500),
            random.randint(100, 500)
        )  # Random mouse movement
        
        # Scroll to trigger lazy-load (realistic speed)
        for _ in range(3):
            await page.mouse.wheel(0, random.randint(300, 500))
            await asyncio.sleep(random.uniform(0.5, 1.5))
        
        # Wait for content to load
        await asyncio.sleep(random.uniform(2, 4))
        
        # Extract inventory data
        inventory = await page.evaluate('''() => {
            return Array.from(document.querySelectorAll('.vehicle-card')).map(card => {
                const vinElement = card.getAttribute('data-vin');
                const titleElement = card.querySelector('.title');
                const priceElement = card.querySelector('.price');
                const mileageElement = card.querySelector('.mileage');
                
                // Extract battery capacity from description
                const description = card.innerText.toLowerCase();
                let kwh = null;
                if (description.includes('75 kwh') || description.includes('75kwh')) kwh = 75;
                else if (description.includes('100 kwh') || description.includes('100kwh')) kwh = 100;
                else if (description.includes('60 kwh')) kwh = 60;
                else if (description.includes('82 kwh')) kwh = 82;
                
                return {
                    vin: vinElement,
                    model: titleElement ? titleElement.innerText : null,
                    price: priceElement ? priceElement.innerText : null,
                    mileage: mileageElement ? mileageElement.innerText : null,
                    battery_kwh: kwh,
                    raw_text: card.innerText.substring(0, 200)  // First 200 chars for debugging
                };
            }).filter(v => v.vin);  // Only return vehicles with VINs
        }''')
        
        logger.info(f"Found {len(inventory)} vehicles in {cluster_name}")
        
        # Generate scan metadata
        scan_metadata = {
            "cluster_name": cluster_name,
            "zip_code": zip_code,
            "timestamp": datetime.utcnow().isoformat(),
            "vehicle_count": len(inventory),
            "ip_strategy": ip_engine.strategy,
            "scan_hash": hashlib.sha256(json.dumps(inventory).encode()).hexdigest()[:16]
        }
        
        return {
            "metadata": scan_metadata,
            "inventory": inventory
        }
        
    except Exception as e:
        logger.error(f"Scan failed for {cluster_name}: {e}")
        return {
            "metadata": {
                "cluster_name": cluster_name,
                "zip_code": zip_code,
                "timestamp": datetime.utcnow().isoformat(),
                "error": str(e)
            },
            "inventory": []
        }
    
    finally:
        await page.close()

# ==========================================
# DATABASE INTEGRATION
# ==========================================

class KineticMeshDB:
    """PostgreSQL integration for kinetic mesh table"""
    
    def __init__(self):
        self.conn = None
        self.cursor = None
    
    def connect(self):
        """Connect to PostgreSQL database"""
        try:
            self.conn = psycopg2.connect(**DB_CONFIG)
            self.cursor = self.conn.cursor()
            logger.info("Connected to PostgreSQL database")
            
            # Create kinetic_mesh table if not exists
            self._create_table()
            
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            raise
    
    def _create_table(self):
        """Create kinetic_mesh table for inventory tracking"""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS kinetic_mesh (
                id SERIAL PRIMARY KEY,
                scan_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                cluster_name VARCHAR(100),
                zip_code VARCHAR(10),
                vin VARCHAR(17) UNIQUE,
                model VARCHAR(200),
                price VARCHAR(50),
                mileage VARCHAR(50),
                battery_kwh INTEGER,
                raw_text TEXT,
                scan_hash VARCHAR(16),
                ip_strategy VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE INDEX IF NOT EXISTS idx_vin ON kinetic_mesh(vin);
            CREATE INDEX IF NOT EXISTS idx_cluster ON kinetic_mesh(cluster_name);
            CREATE INDEX IF NOT EXISTS idx_timestamp ON kinetic_mesh(scan_timestamp);
        """)
        self.conn.commit()
        logger.info("kinetic_mesh table ready")
    
    def insert_scan_results(self, scan_data: Dict):
        """Insert scan results into database"""
        metadata = scan_data["metadata"]
        inventory = scan_data["inventory"]
        
        if not inventory:
            logger.warning(f"No inventory to insert for {metadata['cluster_name']}")
            return
        
        # Prepare data for batch insert
        values = [
            (
                metadata["timestamp"],
                metadata["cluster_name"],
                metadata["zip_code"],
                vehicle["vin"],
                vehicle["model"],
                vehicle["price"],
                vehicle["mileage"],
                vehicle["battery_kwh"],
                vehicle["raw_text"],
                metadata["scan_hash"],
                metadata["ip_strategy"]
            )
            for vehicle in inventory
        ]
        
        # Batch insert with conflict handling
        execute_values(
            self.cursor,
            """
            INSERT INTO kinetic_mesh (
                scan_timestamp, cluster_name, zip_code, vin, model, price, 
                mileage, battery_kwh, raw_text, scan_hash, ip_strategy
            ) VALUES %s
            ON CONFLICT (vin) DO UPDATE SET
                scan_timestamp = EXCLUDED.scan_timestamp,
                price = EXCLUDED.price,
                mileage = EXCLUDED.mileage,
                updated_at = CURRENT_TIMESTAMP
            """,
            values
        )
        
        self.conn.commit()
        logger.info(f"Inserted {len(values)} vehicles into database")
    
    def get_inventory_stats(self) -> Dict:
        """Get current inventory statistics"""
        self.cursor.execute("""
            SELECT 
                COUNT(*) as total_vehicles,
                COUNT(DISTINCT cluster_name) as clusters,
                AVG(battery_kwh) as avg_battery_kwh,
                MAX(scan_timestamp) as last_scan
            FROM kinetic_mesh
        """)
        
        result = self.cursor.fetchone()
        return {
            "total_vehicles": result[0],
            "clusters": result[1],
            "avg_battery_kwh": result[2],
            "last_scan": result[3]
        }
    
    def close(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        logger.info("Database connection closed")

# ==========================================
# MAIN ORCHESTRATION
# ==========================================

async def main_launch():
    """
    Launch National Pulse Agent with IP masking
    """
    print("=" * 60)
    print("🚀 CDLS NATIONAL PULSE AGENT - SOVEREIGN SCRAPING ENGINE")
    print("=" * 60)
    print()
    
    # Initialize IP masking
    ip_engine = IPMaskingEngine(strategy=IP_STRATEGY)
    await ip_engine.initialize()
    
    # Initialize stealth browser
    stealth_browser = StealthBrowser(ip_engine)
    await stealth_browser.launch()
    
    # Initialize database
    db = KineticMeshDB()
    db.connect()
    
    try:
        print(f"📡 Scanning {len(CLUSTERS)} strategic clusters...")
        print(f"🔒 IP Masking: {IP_STRATEGY}")
        print()
        
        # Scan all clusters in parallel (with rate limiting)
        tasks = []
        for cluster_name, zip_code in CLUSTERS.items():
            tasks.append(
                pulse_scan(zip_code, cluster_name, stealth_browser, ip_engine)
            )
            
            # Rate limiting: Don't launch all requests simultaneously
            if len(tasks) >= 3:  # Process 3 at a time
                results = await asyncio.gather(*tasks)
                
                # Store results
                for result in results:
                    db.insert_scan_results(result)
                
                tasks = []
                
                # Delay between batches
                await asyncio.sleep(random.uniform(10, 20))
        
        # Process remaining tasks
        if tasks:
            results = await asyncio.gather(*tasks)
            for result in results:
                db.insert_scan_results(result)
        
        # Print statistics
        print()
        print("=" * 60)
        print("📊 SCAN COMPLETE - INVENTORY STATISTICS")
        print("=" * 60)
        
        stats = db.get_inventory_stats()
        print(f"Total Vehicles: {stats['total_vehicles']}")
        print(f"Clusters Scanned: {stats['clusters']}")
        print(f"Avg Battery Capacity: {stats['avg_battery_kwh']:.1f} kWh")
        print(f"Last Scan: {stats['last_scan']}")
        print()
        print("✅ Data piped to PostgreSQL 'kinetic_mesh' table")
        print("=" * 60)
        
    except Exception as e:
        logger.error(f"Main launch failed: {e}")
        raise
    
    finally:
        # Cleanup
        await stealth_browser.close()
        db.close()
        
        if ip_engine.tor_controller:
            ip_engine.tor_controller.close()

# ==========================================
# INSTALLATION & SETUP INSTRUCTIONS
# ==========================================

def print_installation_guide():
    """Print installation and setup instructions"""
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                   NATIONAL PULSE AGENT - INSTALLATION GUIDE                  ║
╚══════════════════════════════════════════════════════════════════════════════╝

STEP 1: INSTALL CORE DEPENDENCIES
──────────────────────────────────────────────────────────────────────────────
pip install camoufox playwright aiohttp psycopg2-binary python-dotenv stem

# Install Playwright browsers
playwright install firefox

# Fetch Camoufox stealth binary
camoufox fetch


STEP 2: CHOOSE IP MASKING STRATEGY
──────────────────────────────────────────────────────────────────────────────

OPTION A: ROTATING RESIDENTIAL PROXIES (Recommended - Best Stealth)
───────────────────────────────────────────────────────────────────
Provider: WebShare.io (Budget Option - $49/month for 1GB)
1. Sign up: https://www.webshare.io/
2. Create proxy credentials
3. Add to .env file:
   PROXY_PROVIDER=webshare
   WEBSHARE_USER=your_username
   WEBSHARE_PASS=your_password

Alternative Providers:
- SmartProxy: $75/month (https://smartproxy.com/) - Good balance
- BrightData: $500/month (https://brightdata.com/) - Premium
- Oxylabs: $300/month (https://oxylabs.io/) - Mid-tier


OPTION B: TOR NETWORK (Free - Good Stealth, Slower)
───────────────────────────────────────────────────
1. Install Tor:
   Mac: brew install tor
   Linux: sudo apt install tor
   Windows: Download from https://www.torproject.org/

2. Start Tor service:
   Mac/Linux: tor
   Windows: Start from Tor Browser

3. Configure Tor control:
   echo "ControlPort 9051" >> /usr/local/etc/tor/torrc
   echo "HashedControlPassword $(tor --hash-password YOUR_PASSWORD)" >> /usr/local/etc/tor/torrc

4. Add to .env:
   IP_STRATEGY=tor
   TOR_PASSWORD=YOUR_PASSWORD


OPTION C: VPN (Moderate Stealth, Easiest Setup)
───────────────────────────────────────────────
1. Subscribe to VPN service:
   - NordVPN ($12/month): https://nordvpn.com/
   - ExpressVPN ($13/month): https://expressvpn.com/
   - Private Internet Access ($10/month): https://privateinternetaccess.com/

2. Connect VPN at OS level (NordVPN app, etc.)

3. Add to .env:
   IP_STRATEGY=vpn


STEP 3: CONFIGURE DATABASE
──────────────────────────────────────────────────────────────────────────────
1. Install PostgreSQL:
   Mac: brew install postgresql
   Linux: sudo apt install postgresql

2. Create database:
   createdb cdls_kinetic_mesh

3. Add to .env:
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=cdls_kinetic_mesh
   DB_USER=your_postgres_user
   DB_PASSWORD=your_postgres_password


STEP 4: CREATE .ENV FILE
──────────────────────────────────────────────────────────────────────────────
Create file: .env

# IP Masking Strategy
IP_STRATEGY=rotating_proxies  # Options: rotating_proxies, tor, vpn, none

# Proxy Configuration (if using rotating_proxies)
PROXY_PROVIDER=webshare
WEBSHARE_USER=your_username
WEBSHARE_PASS=your_password

# Tor Configuration (if using tor)
TOR_PASSWORD=your_tor_password

# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=cdls_kinetic_mesh
DB_USER=cdls_admin
DB_PASSWORD=your_secure_password


STEP 5: RUN THE AGENT
──────────────────────────────────────────────────────────────────────────────
python national_pulse_agent.py


STEP 6: VERIFY IP MASKING IS WORKING
──────────────────────────────────────────────────────────────────────────────
Check logs for:
✅ "Initialized [provider] proxy"
✅ "Proxy will auto-rotate on next request"
✅ "Stealth browser launched successfully"

Test IP rotation manually:
curl --proxy http://username:password@gate.smartproxy.com:7000 https://api.ipify.org


COST COMPARISON
──────────────────────────────────────────────────────────────────────────────
Strategy              | Monthly Cost | Stealth Level | Speed    | Recommended
──────────────────────────────────────────────────────────────────────────────
Rotating Proxies      | $49-$500     | ⭐⭐⭐⭐⭐     | Fast     | ✅ Best
Tor Network           | $0           | ⭐⭐⭐⭐       | Slow     | Budget option
VPN                   | $10-$13      | ⭐⭐⭐         | Fast     | Easy setup
No Masking            | $0           | ⭐            | Fastest  | ❌ Risky

RECOMMENDATION: Start with WebShare ($49/month) for best stealth/cost balance.


OPSEC BEST PRACTICES
──────────────────────────────────────────────────────────────────────────────
1. ✅ Rotate IP after every 3-5 requests
2. ✅ Add random delays (2-5 seconds) between requests
3. ✅ Randomize browser fingerprints (Camoufox does this automatically)
4. ✅ Never scrape same site from same IP within 1 hour
5. ✅ Use residential proxies (not datacenter IPs)
6. ✅ Respect robots.txt and rate limits
7. ✅ Monitor for CAPTCHAs or blocks (add CAPTCHA solver if needed)

╚══════════════════════════════════════════════════════════════════════════════╝
    """)

# ==========================================
# ENTRY POINT
# ==========================================

if __name__ == "__main__":
    import sys
    
    if "--install-guide" in sys.argv:
        print_installation_guide()
    else:
        asyncio.run(main_launch())
