from typing import List

import psutil as psu
import schemas
from fastapi import APIRouter, Path, Query

router = APIRouter(prefix="/hwinfo", tags=["HWINFO"])

@router.get("/cpu", response_model=schemas.Cpu)
def Cpu():
	'''
	Returns system's CPU crutial stats.\n
	Response model: `Cpu`
	'''
	return {
			"freq": psu.cpu_freq().current,
			"cores": psu.cpu_count(),
			"usage": psu.cpu_percent(0.5)
		}


@router.get("/disks", response_model=List[schemas.Storage])
def Disks():
	'''
	Returns system's partitions and their statistics.\n
	Response model: `List[Storage]`
	'''
	out = []
	for disk in psu.disk_partitions(all=True):
		try:
			diskd = psu.disk_usage(disk.mountpoint)
			out.append({
				"name":    disk.device,
				"unit":    "GiB",
				"used":    round(diskd.used /(1<<30),2),
				"total":   round(diskd.total/(1<<30),2),
				"usage":   round(diskd.percent,2),
				"fsystem": disk.fstype
			}) if diskd.total > 32 * (1<<30) else ...
		except PermissionError:
			...

	return out


@router.get("/memory", response_model=schemas.Storage)
def Memory():
	'''
	Returns system's RAM usage.\n
	Response model: `Storage`
	'''
	ram = psu.virtual_memory()
	return {
			"name": "RAM",
			"unit": "GiB",
			"used": round(ram.used/(1<<30),2),
			"total": round(ram.total/(1<<30),2),
			"usage": round(ram.percent,2)
		}
