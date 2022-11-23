// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

contract AuthenticationOTP {
    struct OneTimePassword {
        uint256 password;
        uint256 validUntill;
    }

    mapping(address => mapping(address => OneTimePassword)) public otp;

    function generateOtp(address user, uint256 validFor) public {
        require(
            validFor <= 600 && validFor >= 30,
            "OTP valid time must be between 30 and 600 seconds"
        );
        otp[user][msg.sender] = OneTimePassword(
            _getNewOtp(),
            block.timestamp + validFor
        );
    }

    function getOtp(address app) public view returns (uint256) {
        return otp[msg.sender][app].password;
    }

    function validatePassword(uint256 password, address user)
        public view returns (bool)
    {
        if (
            otp[user][msg.sender].password == password &&
            otp[user][msg.sender].validUntill >= block.timestamp
        ) {
            return true;
        }
        return false;
    }

    function _getNewOtp() private view returns (uint256) {
        return
            uint256(keccak256(abi.encodePacked(
                blockhash(block.number - 1),
                block.timestamp,
                msg.sender
            )));
    }
}
