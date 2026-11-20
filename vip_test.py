#!/usr/bin/env python3
import json, platform, os, time

def get_system_info():
    info = {
        "system": platform.system(),
        "node": platform.node(),
        "release": platform.release(),
        "processor": platform.processor(),
        "python_version": platform.python_version(),
        "uptime_seconds": int(time.time() - os.stat('/proc/1').st_ctime) if os.path.exists('/proc/1') else None,
        "load_average": os.getloadavg() if hasattr(os, 'getloadavg') else None,
        "environment": dict(os.environ)
    }
    return info

if __name__ == "__main__":
    info = get_system_info()
    print(json.dumps(info, indent=2, ensure_ascii=False))
