import gc
import time
import psutil
from fastapi import FastAPI
from collections import OrderedDict

app = FastAPI(title="NEXUS ENGINE V12 PRO MAX", version="12.0")

class NexusV12_MasterCore:
    """V12 PRO MAX - Real Auto-Heal Engine"""
    
    def __init__(self):
        self.cache = OrderedDict()
        self.heal_count = 0
        self.total_freed = 0
        
        # Test cache bharo
        for i in range(1000):
            self.cache[f"order_{i}"] = "x" * 10240  # 10KB each

    def get_stats(self):
        try:
            vm = psutil.virtual_memory()
            used = vm.used / (1024*1024)
            free = vm.available / (1024*1024)
            cpu = psutil.cpu_percent(interval=0.1)
            return used, free, cpu
        except:
            return 400.0, 624.0, 15.0

    def monitor_and_heal(self, current_ram_mb=None):
        if current_ram_mb:
            used_mb, free_mb, cpu = current_ram_mb, 1024 - current_ram_mb, 85
        else:
            used_mb, free_mb, cpu = self.get_stats()
        
        print(f"[V12] SCAN: Used={used_mb:.0f}MB Free={free_mb:.0f}MB CPU={cpu}% Cache={len(self.cache)}")
        
        if used_mb > 900:
            print(f"[V12] 🔥 CRITICAL {used_mb:.0f}MB! Healing...")
            
            before = len(self.cache)
            
            # REAL HEAL 1: Purge 70% LRU
            purge = int(before * 0.7)
            for _ in range(purge):
                self.cache.popitem(last=False)
            
            # REAL HEAL 2: Garbage Collect
            gc_count = gc.collect()
            
            # REAL HEAL 3: Throttle
            time.sleep(0.1)
            
            after = len(self.cache)
            self.heal_count += 1
            self.total_freed += purge
            
            print(f"[V12] ✅ HEALED_AND_OPTIMIZED")
            print(f"  Purged: {purge} items ({before}->{after})")
            print(f"  GC: {gc_count} objects freed")
            print(f"  Total Heals: {self.heal_count}")
            
            return {
                "status": "HEALED_AND_OPTIMIZED",
                "purged": purge,
                "before": before,
                "after": after,
                "gc_freed": gc_count,
                "heal_count": self.heal_count
            }
        
        print("[V12] ✅ OPTIMAL - Beast Mode")
        return {
            "status": "OPTIMAL",
            "cache": len(self.cache),
            "heal_count": self.heal_count
        }

v12 = NexusV12_MasterCore()

@app.get("/")
def home():
    used, free, cpu = v12.get_stats()
    return {
        "owner": "Abhishek Pal",
        "engine": "NEXUS V12 PRO MAX",
        "status": "LIVE",
        "ram": f"{used:.0f}MB Used",
        "cache": len(v12.cache),
        "heal_count": v12.heal_count
    }

@app.get("/v12-heal")
def heal_now():
    used, free, cpu = v12.get_stats()
    result = v12.monitor_and_heal(used)
    return {
        "system": f"{used:.0f}MB Used / {free:.0f}MB Free / {cpu}% CPU",
        "result": result
    }

@app.get("/v12-critical-test")
def critical_test():
    result = v12.monitor_and_heal(950)
    return {
        "test": "950MB Critical Test",
        "result": result
    }
