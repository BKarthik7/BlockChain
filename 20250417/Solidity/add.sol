pragma solidity ^0.8.26;
// SPDX-License-Identifier: UNLICENSED
contract SolidityTest{
    uint a=10;
    uint b=12;
    uint sum;
    function getResult() public returns(uint){
        sum=a+b;
        return sum;
    }
}