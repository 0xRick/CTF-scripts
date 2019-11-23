pragma solidity ^0.4.24;

contract WeaponizedPing 
{
  string store = "google.com";

  function getDomain() public view returns (string) 
  {
      return store;
  }

  function setDomain(string _value) public 
  {
      store = _value;
  }
}
