"""
Payment Gateway Balance Monitoring System
Monitors fiat balances and NVCT reserves to ensure adequate liquidity
"""

import os
from datetime import datetime, timedelta
from gateway_balance_checker import GatewayBalanceChecker
from account_holder_models import db, BankAccount, CurrencyType
import logging

class GatewayMonitor:
    """Monitor gateway balances and alert on low funds"""
    
    def __init__(self):
        self.min_usd_threshold = {
            'stripe': 10000,      # $10k minimum
            'paypal': 10000,      # $10k minimum  
            'flutterwave': 5000   # $5k minimum
        }
        
        self.min_nvct_threshold = {
            'stripe': 100000,     # 100k NVCT minimum
            'paypal': 100000,     # 100k NVCT minimum
            'flutterwave': 50000, # 50k NVCT minimum
            'nvc_pos': 50000,     # 50k NVCT minimum
            'mojoloop': 50000     # 50k NVCT minimum
        }
    
    def check_nvct_reserves(self):
        """Check NVCT reserve balances for all gateways"""
        gateway_accounts = BankAccount.query.filter(
            BankAccount.account_name.like('%Gateway Reserve%'),
            BankAccount.currency == CurrencyType.NVCT
        ).all()
        
        alerts = []
        reserves_status = {}
        
        for account in gateway_accounts:
            gateway_name = self._extract_gateway_name(account.account_name)
            threshold = self.min_nvct_threshold.get(gateway_name, 50000)
            
            reserves_status[gateway_name] = {
                'current_balance': float(account.balance),
                'available_balance': float(account.available_balance),
                'threshold': threshold,
                'status': 'OK' if account.balance >= threshold else 'LOW',
                'account_id': account.id
            }
            
            if account.balance < threshold:
                alerts.append({
                    'type': 'LOW_NVCT_RESERVE',
                    'gateway': gateway_name,
                    'current': account.balance,
                    'threshold': threshold,
                    'account_id': account.id,
                    'severity': 'HIGH' if account.balance < (threshold * 0.5) else 'MEDIUM'
                })
        
        return reserves_status, alerts
    
    def check_fiat_balances(self):
        """Check actual fiat balances in payment gateways"""
        checker = GatewayBalanceChecker()
        results = checker.check_all_gateway_balances()
        
        alerts = []
        fiat_status = {}
        
        for gateway, result in results.items():
            if gateway == 'summary':
                continue
                
            if result.get('success'):
                usd_balance = result.get('total_usd', 0)
                threshold = self.min_usd_threshold.get(gateway, 5000)
                
                fiat_status[gateway] = {
                    'usd_balance': usd_balance,
                    'threshold': threshold,
                    'status': 'OK' if usd_balance >= threshold else 'LOW',
                    'last_checked': result.get('last_checked')
                }
                
                if usd_balance < threshold:
                    alerts.append({
                        'type': 'LOW_FIAT_BALANCE',
                        'gateway': gateway,
                        'current_usd': usd_balance,
                        'threshold': threshold,
                        'severity': 'HIGH' if usd_balance < (threshold * 0.3) else 'MEDIUM'
                    })
            else:
                fiat_status[gateway] = {
                    'status': 'CONNECTION_ERROR',
                    'error': result.get('message'),
                    'last_checked': datetime.now().isoformat()
                }
                
                alerts.append({
                    'type': 'GATEWAY_CONNECTION_ERROR',
                    'gateway': gateway,
                    'error': result.get('message'),
                    'severity': 'HIGH'
                })
        
        return fiat_status, alerts
    
    def _extract_gateway_name(self, account_name):
        """Extract gateway name from account name"""
        name_lower = account_name.lower()
        if 'stripe' in name_lower:
            return 'stripe'
        elif 'paypal' in name_lower:
            return 'paypal'
        elif 'flutterwave' in name_lower:
            return 'flutterwave'
        elif 'pos' in name_lower or 'nvc' in name_lower:
            return 'nvc_pos'
        elif 'mojoloop' in name_lower:
            return 'mojoloop'
        return 'unknown'
    
    def generate_monitoring_report(self):
        """Generate comprehensive monitoring report"""
        nvct_status, nvct_alerts = self.check_nvct_reserves()
        fiat_status, fiat_alerts = self.check_fiat_balances()
        
        all_alerts = nvct_alerts + fiat_alerts
        
        # Calculate total liquidity
        total_nvct_reserves = sum(
            status['current_balance'] for status in nvct_status.values()
        )
        total_fiat_usd = sum(
            status.get('usd_balance', 0) for status in fiat_status.values()
            if status.get('usd_balance') is not None
        )
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_nvct_reserves': total_nvct_reserves,
                'total_fiat_usd': total_fiat_usd,
                'total_alerts': len(all_alerts),
                'high_severity_alerts': len([a for a in all_alerts if a.get('severity') == 'HIGH'])
            },
            'nvct_reserves': nvct_status,
            'fiat_balances': fiat_status,
            'alerts': all_alerts,
            'recommendations': self._generate_recommendations(all_alerts, nvct_status, fiat_status)
        }
        
        return report
    
    def _generate_recommendations(self, alerts, nvct_status, fiat_status):
        """Generate actionable recommendations based on monitoring results"""
        recommendations = []
        
        # Check for low NVCT reserves
        low_nvct = [a for a in alerts if a.get('type') == 'LOW_NVCT_RESERVE']
        if low_nvct:
            recommendations.append({
                'type': 'REFILL_NVCT_RESERVES',
                'priority': 'HIGH',
                'action': 'Use Treasury Operations to mint additional NVCT tokens and fund gateway reserves',
                'affected_gateways': [a['gateway'] for a in low_nvct]
            })
        
        # Check for low fiat balances
        low_fiat = [a for a in alerts if a.get('type') == 'LOW_FIAT_BALANCE']
        if low_fiat:
            recommendations.append({
                'type': 'FUND_FIAT_ACCOUNTS',
                'priority': 'HIGH',
                'action': 'Transfer USD funds to payment gateway accounts to maintain operational liquidity',
                'affected_gateways': [a['gateway'] for a in low_fiat]
            })
        
        # Check for connection errors
        connection_errors = [a for a in alerts if a.get('type') == 'GATEWAY_CONNECTION_ERROR']
        if connection_errors:
            recommendations.append({
                'type': 'FIX_GATEWAY_CONNECTIONS',
                'priority': 'MEDIUM',
                'action': 'Verify API credentials and network connectivity for affected gateways',
                'affected_gateways': [a['gateway'] for a in connection_errors]
            })
        
        return recommendations

def run_monitoring_check():
    """Run a complete monitoring check and return results"""
    monitor = GatewayMonitor()
    return monitor.generate_monitoring_report()

if __name__ == "__main__":
    # Run monitoring check
    report = run_monitoring_check()
    
    print("=== GATEWAY MONITORING REPORT ===")
    print(f"Generated: {report['timestamp']}")
    print(f"Total NVCT Reserves: {report['summary']['total_nvct_reserves']:,.2f}")
    print(f"Total Fiat USD: ${report['summary']['total_fiat_usd']:,.2f}")
    print(f"Active Alerts: {report['summary']['total_alerts']}")
    
    if report['alerts']:
        print("\n=== ALERTS ===")
        for alert in report['alerts']:
            print(f"[{alert.get('severity', 'LOW')}] {alert['type']}: {alert.get('gateway', 'N/A')}")
    
    if report['recommendations']:
        print("\n=== RECOMMENDATIONS ===")
        for rec in report['recommendations']:
            print(f"[{rec['priority']}] {rec['type']}: {rec['action']}")