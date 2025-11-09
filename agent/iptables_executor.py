import subprocess
import re
from typing import List, Dict, Optional


class IptablesExecutor:
    """Wrapper for executing iptables commands safely"""
    
    @staticmethod
    def add_rule(chain: str, action: str, protocol: Optional[str] = None,
                 source_ip: Optional[str] = None, destination_ip: Optional[str] = None,
                 port: Optional[int] = None) -> Dict:
        """
        Add an iptables rule
        
        Args:
            chain: INPUT, OUTPUT, or FORWARD
            action: ACCEPT, DROP, REJECT
            protocol: tcp, udp, icmp (optional)
            source_ip: Source IP address (optional)
            destination_ip: Destination IP address (optional)
            port: Port number (optional)
        
        Returns:
            Dict with status and message
        """
        try:
            cmd = ["sudo", "iptables", "-A", chain, "-j", action]
            
            if protocol:
                cmd.extend(["-p", protocol])
            if source_ip:
                cmd.extend(["-s", source_ip])
            if destination_ip:
                cmd.extend(["-d", destination_ip])
            if port and protocol:
                cmd.extend(["--dport", str(port)])
            
            subprocess.run(cmd, check=True, capture_output=True)
            return {"status": "success", "message": f"Rule added to {chain}"}
        except subprocess.CalledProcessError as e:
            return {"status": "error", "message": str(e)}
    
    @staticmethod
    def delete_rule(chain: str, action: str, protocol: Optional[str] = None,
                    source_ip: Optional[str] = None, destination_ip: Optional[str] = None,
                    port: Optional[int] = None) -> Dict:
        """Delete an iptables rule"""
        try:
            cmd = ["sudo", "iptables", "-D", chain, "-j", action]
            
            if protocol:
                cmd.extend(["-p", protocol])
            if source_ip:
                cmd.extend(["-s", source_ip])
            if destination_ip:
                cmd.extend(["-d", destination_ip])
            if port and protocol:
                cmd.extend(["--dport", str(port)])
            
            subprocess.run(cmd, check=True, capture_output=True)
            return {"status": "success", "message": f"Rule deleted from {chain}"}
        except subprocess.CalledProcessError as e:
            return {"status": "error", "message": str(e)}
    
    @staticmethod
    def list_rules(chain: Optional[str] = None) -> Dict:
        """List iptables rules"""
        try:
            if chain:
                cmd = ["sudo", "iptables", "-L", chain, "-n", "-v"]
            else:
                cmd = ["sudo", "iptables", "-L", "-n", "-v"]
            
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            return {"status": "success", "rules": result.stdout}
        except subprocess.CalledProcessError as e:
            return {"status": "error", "message": str(e)}
    
    @staticmethod
    def flush_chain(chain: str) -> Dict:
        """Flush all rules from a chain"""
        try:
            cmd = ["sudo", "iptables", "-F", chain]
            subprocess.run(cmd, check=True, capture_output=True)
            return {"status": "success", "message": f"Chain {chain} flushed"}
        except subprocess.CalledProcessError as e:
            return {"status": "error", "message": str(e)}
    
    @staticmethod
    def save_rules() -> Dict:
        """Save iptables rules (persistent across reboot)"""
        try:
            subprocess.run(["sudo", "iptables-save"], check=True, capture_output=True)
            return {"status": "success", "message": "Rules saved"}
        except subprocess.CalledProcessError as e:
            return {"status": "error", "message": str(e)}
