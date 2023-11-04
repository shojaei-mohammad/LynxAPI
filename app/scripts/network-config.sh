#!/bin/bash
# network-config.sh

# Log file path
LOG_FILE="/var/log/network-config.log"

# Function to log messages
log() {
    echo "$(date +"%Y-%m-%d %T") : $1" | tee -a $LOG_FILE
}

# Function to validate IP address format
validate_ip() {
    if ! [[ $1 =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
        log "Invalid IP address format: $1"
        exit 1
    fi
}

# Function to validate subnet mask as a CIDR prefix length (0-32)
validate_subnet() {
    if ! [[ $1 =~ ^[0-9]$|^1[0-9]$|^2[0-9]$|^3[0-2]$|^0$ ]]; then
        log "Invalid subnet prefix length: $1. Must be between 0 and 32."
        exit 1
    fi
}


# Function to validate DNS servers
validate_dns() {
    for dns in $1; do
        validate_ip $dns
    done
}

# Assign first argument to variable
INTERFACE=$1
MODE=$2 # 'dhcp' or 'static'

# Log starting
log "Starting network configuration for $INTERFACE"

# Check for mode and apply configurations accordingly
if [ "$MODE" == "dhcp" ]; then
    # Apply DHCP configuration
    dhclient -r $INTERFACE
    if dhclient $INTERFACE; then
        log "DHCP configuration applied successfully for $INTERFACE"
    else
        log "Failed to apply DHCP configuration for $INTERFACE"
        exit 1
    fi
elif [ "$MODE" == "static" ]; then
    # Remaining arguments for static configuration
    IP_ADDRESS=$3
    SUBNET_PREFIX=$4 # This is now the CIDR prefix length
    DNS_SERVERS=$5
    GATEWAY=$6 # New variable for gateway

    # Validate the inputs
    validate_ip $IP_ADDRESS
    validate_subnet $SUBNET_PREFIX
    validate_dns "$DNS_SERVERS"

    # Apply the static IP configuration
    ip addr flush dev $INTERFACE
    ip addr add $IP_ADDRESS/$SUBNET_PREFIX dev $INTERFACE

    # Set the default gateway if specified
    if [ ! -z "$GATEWAY" ]; then
        ip route add default via $GATEWAY
    fi
else
    log "Invalid mode specified: $MODE. Use 'dhcp' or 'static'."
    exit 1
fi

exit 0
