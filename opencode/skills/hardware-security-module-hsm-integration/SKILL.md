---
name: hardware-security-module-hsm-integration
description: >-
  Use this skill when the user is working on or asking about HSM, hardware security module, secure key storage, code signing with HSM, or cryptographic hardware for audio plugins.
version: 1.0.0
---

# SKILL: Hardware Security Module (HSM) Integration

## CAPABILITIES
- Integrate USB-based or embedded HSMs for cryptographic key storage
- Implement secure key derivation and license validation protocols
- Create challenge-response authentication mechanisms for anti-piracy
- Support secure boot and firmware signing for hardware products
- Enable offline license validation while maintaining security

## CAPABILITY TAXONOMY
| Input | Output |
|-------|--------|
| Security requirements (threat model, protection goals) | HSM selection and integration architecture |
| Cryptographic algorithms (symmetric, asymmetric, hashing) | API wrapper and implementation |
| License validation requirements | Secure validation protocol implementation |
| Hardware interface specifications (USB, SPI, I2C) | Low-level communication drivers |
| Performance requirements (latency, throughput) | Optimized cryptographic operations |

## IMPLEMENTATION PATTERN

```cpp
// HSM Integration Example using YubiHSM2 or Nitrokey-like device
#include <cryptohsm.h>  // Hypothetical HSM abstraction layer
#include <openssl/evp.h>
#include <openssl/hmac.h>
#include <openssl/rand.h>

// HSM wrapper class
class AudioHSM {
public:
    AudioHSM() : hsmSession(0) {}
    
    bool initialize() {
        // Connect to HSM device
        if (!hsmConnect()) {
            return false;
        }
        
        // Open session
        hsmSession = hsmOpenSession();
        if (hsmSession == 0) {
            hsmDisconnect();
            return false;
        }
        
        // Authenticate to HSM
        if (!hsmAuthenticate(hsmSession, authKey, authKeyLength)) {
            hsmCloseSession(hsmSession);
            hsmDisconnect();
            return false;
        }
        
        return true;
    }
    
    void cleanup() {
        if (hsmSession != 0) {
            hsmCloseSession(hsmSession);
            hsmSession = 0;
        }
        hsmDisconnect();
    }
    
    // Secure key storage
    bool storeKey(const std::string& keyName, const std::vector<uint8_t>& keyData) {
        return hsmStoreKey(hsmSession, keyName.c_str(), 
                          keyName.length(), 
                          keyData.data(), keyData.size());
    }
    
    bool retrieveKey(const std::string& keyName, std::vector<uint8_t>& keyData) {
        uint32_t keyLength = 0;
        bool result = hsmGetKeyLength(hsmSession, keyName.c_str(), keyName.length(), &keyLength);
        if (!result) return false;
        
        keyData.resize(keyLength);
        return hsmGetKey(hsmSession, keyName.c_str(), keyName.length(),
                        keyData.data(), &keyLength);
    }
    
    // License validation using HSM-protected key
    bool validateLicense(const std::vector<uint8_t>& licenseData,
                        const std::vector<uint8_t>& signature) {
        // Retrieve public key from HSM (private key never leaves HSM)
        std::vector<uint8_t> publicKey;
        if (!retrieveKey("license_public", publicKey)) {
            return false;
        }
        
        // Verify signature using HSM (if supported) or externally with retrieved public key
        // For maximum security, verification should happen inside HSM
        return hsmVerifySignature(hsmSession, 
                                 "license_key",  // Key identifier in HSM
                                 licenseData.data(), licenseData.size(),
                                 signature.data(), signature.size());
    }
    
    // Challenge-response authentication
    bool authenticateChallenge(const std::vector<uint8_t>& challenge,
                              std::vector<uint8_t>& response) {
        return hsmComputeHMAC(hsmSession,
                             "auth_key",     // HMAC key in HSM
                             challenge.data(), challenge.size(),
                             response);
    }
    
    // Secure nonce generation
    bool getSecureNonce(std::vector<uint8_t>& nonce, size_t length) {
        nonce.resize(length);
        return hsmGetRandom(hsmSession, nonce.data(), length);
    }
    
    // Key derivation (using HSM if supported, otherwise externally with protected key)
    bool deriveKey(const std::string& baseKeyName,
                  const std::vector<uint8_t>& salt,
                  const std::vector<uint8_t>& info,
                  std::vector<uint8_t>& derivedKey,
                  size_t keyLength) {
        std::vector<uint8_t> baseKey;
        if (!retrieveKey(baseKeyName, baseKey)) {
            return false;
        }
        
        // Use HKDF or similar (could be done in HSM if supported)
        return hkdf_sha256(baseKey.data(), baseKey.size(),
                          salt.data(), salt.size(),
                          info.data(), info.size(),
                          derivedKey.data(), keyLength);
    }

private:
    HSM_SESSION hsmSession;
    std::vector<uint8_t> authKey;  // Authentication key for HSM access
};
```

## EDGE CASES & FALLBACKS
- **HSM Not Found**: Fall back to software-based obfuscation (less secure) with clear user notification
- **Communication Failure**: Implement retry mechanisms with exponential backoff
- **HSM Locked**: Provide user-guided recovery process (typically requires physical interaction)
- **Performance Bottleneck**: Cache non-sensitive results; batch operations where possible
- **Firmware Updates**: Ensure HSM firmware can be updated without losing keys
- **Side-Channel Attacks**: Use constant-time implementations for cryptographic operations
- **Key Extraction via Power Analysis**: Select HSMs with resistance to differential power analysis (DPA)
- **Fault Injection Attacks**: Use HSMs with fault detection and response mechanisms
- **Supply Chain Attacks**: Implement HSM attestation to verify genuine device

## INTEGRATION POINTS
- HSM Devices: YubiHSM 2, Nitrokey HSM, SoloKeys Solo, Trusted Platform Module (TPM 2.0)
- USB Interfaces: USB CCID, USB HID, USB CDC ACM, custom USB endpoints
- Embedded Interfaces: SPI, I2C, UART, GPIO
- Cryptographic Libraries: OpenSSL, mbed TLS, WolfSSL, BoringSSL
- Key Standards: PKCS#11, FIDO/U2F, WebAuthn, FIDO2
- Secure Elements: ATECC608A, ATECC508A, MAX32520, STSAFE-A110
- Frameworks: Microsoft CryptoAPI, Apple Common Crypto, Android Keystore
- Protocols: Challenge-Response, Mutual TLS, Secure Remote Password (SRP)
- Development Tools: HSM SDKs, PKCS#11 explorers, smart card terminals
- Testing: Cryptographic test vectors, side-channel analysis tools, fault injection frameworks

## EXECUTION EXAMPLES

**Input:** "Implement secure license validation using HSM-stored private key"
**Output:**
```cpp
// Secure license validation with HSM
bool validateLicenseWithHSM(const std::vector<uint8_t>& licenseData,
                         const std::vector<uint8_t>& signature) {
    AudioHSM hsm;
    if (!hsm.initialize()) {
        // Fall back to software verification (less secure)
        // In production, you might want to fail closed instead
        return validateLicenseSoftwareFallback(licenseData, signature);
    }
    
    bool isValid = hsm.validateLicense(licenseData, signature);
    hsm.cleanup();
    return isValid;
}

// Example license data structure
struct LicenseData {
    uint32_t productID;
    uint32_t version;
    uint64_t expiration;  // Timestamp
    uint64_t hardwareID;  // Hash of hardware characteristics
    std::vector<uint8_t> encryptedFeatures;  // AES-GCM encrypted
};

// Signing process (done offline during license generation)
std::vector<uint8_t> generateLicenseSignature(const LicenseData& license) {
    // Serialize license data
    std::vector<uint8_t> serialized = serializeLicense(license);
    
    // Sign with private key (held securely, never in software)
    // This would typically be done on a secure signing server
    // that has access to the HSM or uses the HSM directly
    return signWithHSM(serialized);
}
```

**Input:** "Create a secure firmware update system using HSM-stored signing key"
**Output:**
```cpp
// Secure firmware update verification
bool verifyFirmwareSignature(const std::vector<uint8_t>& firmware,
                            const std::vector<uint8_t>& signature) {
    AudioHSM hsm;
    if (!hsm.initialize()) {
        return false;  // Fail closed if HSM unavailable
    }
    
    bool isValid = hsm.verifySignature(
        "firmware_key",  // Key identifier in HSM
        firmware.data(), firmware.size(),
        signature.data(), signature.size());
    
    hsm.cleanup();
    return isValid;
}

// Firmware update process
bool applyFirmwareUpdate(const std::vector<uint8_t>& newFirmware,
                        const std::vector<uint8_t>& signature) {
    // 1. Verify signature
    if (!verifyFirmwareSignature(newFirmware, signature)) {
        return false;  // Invalid signature
    }
    
    // 2. Verify version number (optional but recommended)
    uint32_t newVersion = extractFirmwareVersion(newFirmware);
    uint32_t currentVersion = getCurrentFirmwareVersion();
    if (newVersion <= currentVersion) {
        return false;  // Downgrade protection
    }
    
    // 3. Apply update (hardware-specific)
    return flashFirmware(newFirmware);
}
```