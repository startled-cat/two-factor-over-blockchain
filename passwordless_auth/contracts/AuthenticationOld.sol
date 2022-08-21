// SPDX-License-Identifier: MIT
pragma solidity >=0.1.2;

contract Authentication {
    struct Token {
        address user;
        address app;
        uint256 validUntill;
    }

    Token[] tokens;

    function createToken(address app, uint256 tokenValidTime) public {
        require(
            tokenValidTime <= 600 && tokenValidTime >= 30,
            "Access time must be between 30 and 600 seconds"
        );
        require(app != msg.sender, "App address can't be equal to msg.sender");
        (uint256 tokenIndex, bool exists) = _findToken(msg.sender, app);
        if (!exists) {
            tokens.push(
                Token(msg.sender, app, block.timestamp + tokenValidTime)
            );
        } else {
            tokens[tokenIndex].validUntill = block.timestamp + tokenValidTime;
        }
    }

    function checkToken(address user, address app) public view returns (bool) {
        (uint256 i, bool exists) = _findToken(user, app);
        if (!exists) {
            return false;
        }
        return _isTokenValid(i);
    }

    function receiveToken(address user) public {
        (uint256 i, bool exists) = _findToken(user, msg.sender);
        require(exists, "Token does not exist");
        require(_isTokenValid(i), "Token has expired");
        _removeToken(i);
    }

    function _isTokenValid(uint256 tokenIndex) private view returns (bool) {
        return tokens[tokenIndex].validUntill >= block.timestamp;
    }

    function _findToken(address user, address app)
        private view returns (uint256 _index, bool _exists)
    {
        for (_index = 0; _index < tokens.length; _index++) {
            if (tokens[_index].user == user && tokens[_index].app == app) {
                return (_index, true);
            }
        }
        return (_index, false);
    }

    function _removeToken(uint256 index) private {
        require(index < tokens.length, "Index out of bounds");
        if (tokens.length > 1 && index != tokens.length - 1) {
            tokens[index] = tokens[tokens.length - 1];
        }
        tokens.pop();
    }
}
