// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.8.0 ;


contract RootClass{
    function _Address_to_String(address _addr) internal pure returns(string memory) {
        bytes memory data = abi.encodePacked(_addr);
        bytes memory alphabet = "0123456789abcdef";

        bytes memory str = new bytes(2 + data.length * 2);
        str[0] = "0";
        str[1] = "x";
        for (uint i = 0; i < data.length; i++) {
            str[2+i*2] = alphabet[uint(uint8(data[i] >> 4))];
            str[3+i*2] = alphabet[uint(uint8(data[i] & 0x0f))];
        }
        return string(str);
    }

    function _String_to_Address(string memory _a) internal pure returns (address _parsedAddress) {
        bytes memory tmp = bytes(_a);
        uint160 iaddr = 0;
        uint160 b1;
        uint160 b2;
        for (uint i = 2; i < 2 + 2 * 20; i += 2) {
            iaddr *= 256;
            b1 = uint160(uint8(tmp[i]));
            b2 = uint160(uint8(tmp[i + 1]));
            if ((b1 >= 97) && (b1 <= 102)) {
                b1 -= 87;
            } else if ((b1 >= 65) && (b1 <= 70)) {
                b1 -= 55;
            } else if ((b1 >= 48) && (b1 <= 57)) {
                b1 -= 48;
            }
            if ((b2 >= 97) && (b2 <= 102)) {
                b2 -= 87;
            } else if ((b2 >= 65) && (b2 <= 70)) {
                b2 -= 55;
            } else if ((b2 >= 48) && (b2 <= 57)) {
                b2 -= 48;
            }
            iaddr += (b1 * 16 + b2);
        }
        return address(iaddr);
    }
}

contract Repository is RootClass{
    string state;
    string public repo_name;
    address owner;
    address[] private address_whitelist;

    constructor(string memory _name){
        owner = msg.sender;
        address_whitelist.push(msg.sender);
        repo_name = _name;
    }

    modifier onlyOwner() {
        require(msg.sender == owner,
                "Only owner can execute!");
        _;
    }

    modifier onlyWhiteList() {
        uint counter = 0;
        for (uint i=0; i<address_whitelist.length; i++) {
            if(msg.sender==address_whitelist[i]){counter++;}
        }
        require(counter >= 1,
                "Only whitelisted address can execute!");
        _;
    }

    function whitelist(string memory _addr_str) public onlyOwner{
        address _addr = _String_to_Address(_addr_str);
        address_whitelist.push(_addr);
    }

    function whitelist_remove(string memory _addr_str) public onlyOwner{
        uint counter = 0;
        address _addr = _String_to_Address(_addr_str);
        for (uint i=0; i<address_whitelist.length; i++) {
            if(address_whitelist[i] == _addr){counter++;}
        }
        require(counter >= 1,
                "Address is not in whitelist.");
        for (uint i=0; i<address_whitelist.length; i++) {
            if(address_whitelist[i] == _addr){delete address_whitelist[i];}
        }
    }


    function git_pull() public onlyWhiteList view returns (string memory) {
        return state;
    }

    function git_push(string memory _state) public onlyWhiteList {
        state = _state;
    }

    function name() public view returns (string memory){
        return repo_name;
    }

    function rename(string memory _name) public onlyOwner{
        repo_name = _name;
    }
}
