pragma solidity ^0.4.22;

contract ChainsawClub {

  string username = 'nobody';
  string password = '7b455ca1ffcb9f3828cfdde4a396139e';
  bool approve = false;
  uint totalSupply = 1000;
  uint userBalance = 0;

  function getUsername() public view returns (string) {
      return username;
  }
  function setUsername(string _value) public {
      username = _value;
  }
  function getPassword() public view returns (string) {
      return password;
  }
  function setPassword(string _value) public {
      password = _value;
  }
  function getApprove() public view returns (bool) {
      return approve;
  }
  function setApprove(bool _value) public {
      approve = _value;
  }
  function getSupply() public view returns (uint) {
      return totalSupply;
  }
  function getBalance() public view returns (uint) {
      return userBalance;
  }
  function transfer(uint _value) public {
      if (_value > 0 && _value <= totalSupply) {
          totalSupply -= _value;
          userBalance += _value;
      }
  }
  function reset() public {
      username = '';
      password = '';
      userBalance = 0;
      totalSupply = 1000;
      approve = false;
  }
}
