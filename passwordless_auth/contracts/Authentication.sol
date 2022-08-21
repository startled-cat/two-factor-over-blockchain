// SPDX-License-Identifier: MIT
pragma solidity >=0.1.2;

contract Authentication {
    mapping(address => mapping(address => uint256)) public tokens;

    function createToken(address app, uint256 tokenValidTime) public {
        require(
            tokenValidTime <= 600 && tokenValidTime >= 30,
            "Access time must be between 30 and 600 seconds"
        );
        require(app != msg.sender, "App address can't be equal to msg.sender");
        tokens[msg.sender][app] = block.timestamp + tokenValidTime;
    }

    function checkToken(address user, address app) public view returns (bool) {
        return _isTokenValid(user, app);
    }

    function receiveToken(address user) public {
        require(_findToken(user, msg.sender), "Token does not exist");
        require(_isTokenValid(user, msg.sender), "Token has expired");
        _removeToken(user, msg.sender);
    }

    function _findToken(address user, address app)
        private view returns (bool _exists)
    {
        return tokens[user][app] != 0;
    }

    function _removeToken(address user, address app) private {
        tokens[user][app] = 0;
    }

    function _isTokenValid(address user, address app)
        private view returns (bool)
    {
        return tokens[user][app] >= block.timestamp;
    }
}
