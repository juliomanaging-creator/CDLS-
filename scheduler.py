"""
Scheduler
Keeps the Anthropic Knowledge Base automatically updated.
Runs incremental scrapes on a configurable schedule.
"""

import asyncio
import signal
import sys
from datetime import datetime, timedelta
from utils.logger import setup_logger

logger = setup_logger("scheduler")


class KBScheduler:
    """
    Automated scheduler that keeps the knowledge base current.
    
    Default schedule:
    - Full rebuild: Weekly (Sundays at 2am)
    - Incremental update: Daily at midnight
    - Quick news check: Every 6 hours (anthropic.com/news)
    """

    def __init__(self, orchestrator, config: dict):
        self.orchestrator = orchestrator
        self.config = config
        self.running = False
        self.tasks = []
        self.stats = {
            "full_rebuilds": 0,
            "incremental_updates": 0,
            "news_checks": 0,
            "last_full_rebuild": None,
            "last_update": None,
            "errors": 0,
        }

    def start(self):
        """Start the scheduler."""
        logger.info("Starting Knowledge Base Scheduler")
        logger.info("  Full rebuild:     Weekly (Sunday 2am)")
        logger.info("  Incremental:      Daily midnight")
        logger.info("  News check:       Every 6 hours")

        self.running = True

        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._shutdown_handler)
        signal.signal(signal.SIGTERM, self._shutdown_handler)

        asyncio.run(self._run())

    async def _run(self):
        """Main scheduler loop."""
        # Create scheduled tasks
        self.tasks = [
            asyncio.create_task(self._weekly_full_rebuild()),
            asyncio.create_task(self._daily_incremental_update()),
            asyncio.create_task(self._hourly_news_check()),
            asyncio.create_task(self._health_monitor()),
        ]

        logger.info("Scheduler running. Press Ctrl+C to stop.")
        try:
            await asyncio.gather(*self.tasks)
        except asyncio.CancelledError:
            logger.info("Scheduler tasks cancelled")

    async def _weekly_full_rebuild(self):
        """Run a complete KB rebuild every week."""
        while self.running:
            now = datetime.now()
            # Calculate seconds until next Sunday 2am
            days_until_sunday = (6 - now.weekday()) % 7
            if days_until_sunday == 0 and now.hour >= 2:
                days_until_sunday = 7
            next_run = now.replace(hour=2, minute=0, second=0, microsecond=0)
            next_run += timedelta(days=days_until_sunday)
            wait_seconds = (next_run - now).total_seconds()

            logger.info(f"Next full rebuild scheduled: {next_run.strftime('%Y-%m-%d %H:%M')}")
            await asyncio.sleep(wait_seconds)

            if not self.running:
                break

            try:
                logger.info("=" * 50)
                logger.info("WEEKLY FULL REBUILD STARTING")
                logger.info("=" * 50)
                await self.orchestrator.run_full_pipeline()
                self.stats["full_rebuilds"] += 1
                self.stats["last_full_rebuild"] = datetime.now().isoformat()
                logger.info("Weekly full rebuild complete")
            except Exception as e:
                logger.error(f"Full rebuild failed: {e}")
                self.stats["errors"] += 1

    async def _daily_incremental_update(self):
        """Run incremental update daily at midnight."""
        while self.running:
            now = datetime.now()
            next_midnight = (now + timedelta(days=1)).replace(
                hour=0, minute=0, second=0, microsecond=0
            )
            wait_seconds = (next_midnight - now).total_seconds()

            await asyncio.sleep(wait_seconds)

            if not self.running:
                break

            try:
                logger.info("Running daily incremental update...")
                await self.orchestrator.update_kb()
                self.stats["incremental_updates"] += 1
                self.stats["last_update"] = datetime.now().isoformat()
            except Exception as e:
                logger.error(f"Incremental update failed: {e}")
                self.stats["errors"] += 1

    async def _hourly_news_check(self):
        """Check for new Anthropic announcements every 6 hours."""
        news_sources = [
            "https://www.anthropic.com/news",
            "https://www.anthropic.com/research",
        ]
        while self.running:
            await asyncio.sleep(6 * 3600)  # 6 hours

            if not self.running:
                break

            try:
                logger.info("Checking for new Anthropic announcements...")
                for source in news_sources:
                    await self.orchestrator.update_kb(source_url=source)
                self.stats["news_checks"] += 1
            except Exception as e:
                logger.error(f"News check failed: {e}")
                self.stats["errors"] += 1

    async def _health_monitor(self):
        """Log health stats every hour."""
        while self.running:
            await asyncio.sleep(3600)
            stats = await self.orchestrator.db.get_statistics()
            logger.info(
                f"KB Health: {stats.get('total_documents', 0)} docs | "
                f"Rebuilds: {self.stats['full_rebuilds']} | "
                f"Updates: {self.stats['incremental_updates']} | "
                f"Errors: {self.stats['errors']}"
            )

    def _shutdown_handler(self, signum, frame):
        """Graceful shutdown on SIGINT/SIGTERM."""
        logger.info("\nShutdown signal received, stopping scheduler...")
        self.running = False
        for task in self.tasks:
            task.cancel()
        sys.exit(0)

    def get_stats(self) -> dict:
        """Return current scheduler statistics."""
        return {
            **self.stats,
            "scheduler_running": self.running,
            "checked_at": datetime.now().isoformat(),
        }


async def run_once(orchestrator):
    """Run a single pipeline execution without scheduling."""
    logger.info("Running one-time pipeline execution...")
    await orchestrator.run_full_pipeline()


if __name__ == "__main__":
    from config.settings import load_config
    from orchestrator import OrchestratorAgent

    config = load_config()
    orchestrator = OrchestratorAgent(config)

    scheduler = KBScheduler(orchestrator, config)
    scheduler.start()
