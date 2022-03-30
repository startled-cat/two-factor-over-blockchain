// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

contract AuthenticatorProvider {
    address owner;
    uint32 otpValidFor;

    uint256 passwordSeed = 123456789;

    struct OneTimePassword {
        uint256 password;
        uint256 generatedAt;
    }

    mapping(address => OneTimePassword) public otp;

    event OtpValidationFailed(address user, uint256 timestamp, string reason);

    constructor() {
        owner = msg.sender;
        otpValidFor = 30;
    }

    // internal
    // should generate random string of characters - one time password
    function getNewOtp() public view returns (uint256) {
        // not actually random, just for testing
        return
            uint256(
                keccak256(
                    abi.encodePacked(
                        blockhash(block.number - 1),
                        block.timestamp,
                        msg.sender
                    )
                )
            );
    }

    // only owner
    // authenticator service would call this function to generate one time passowrd for a given user
    function generateOtp(address for_user) public {
        if (msg.sender == owner) {
            otp[for_user] = OneTimePassword(getNewOtp(), block.timestamp);
        }
    }

    // user would call this function to retrieve one time password
    function getOtp() public view returns (uint256) {
        return otp[msg.sender].password;
    }

    // only owner
    // once users enters otp, service would call this function to validate it
    // returns 0 => password valid; 1 => incorrect password, 2 => password expired
    // todo: handle situation when password wasnt generated before (there is no mapping for user in otp)
    function validatePassword(uint256 password, address user)
        public
        view
        returns (uint256)
    {
        if (otp[user].password != password) {
            return 1;
        }
        if ((otp[user].generatedAt + otpValidFor) < block.timestamp) {
            return 2;
        }
        return 0;
    }
}
