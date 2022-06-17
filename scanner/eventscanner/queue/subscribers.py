from pubsub import pub

from scanner.eventscanner.monitors.payments.duc_payment_monitor import DucPaymentMonitor
from scanner.eventscanner.monitors.payments.duc_transfer_monitor import DucTransferMonitor


pub.subscribe(DucPaymentMonitor.on_new_block_event, 'DUCATUS_MAINNET')
pub.subscribe(DucTransferMonitor.on_new_block_event, 'DUCATUS_MAINNET')
