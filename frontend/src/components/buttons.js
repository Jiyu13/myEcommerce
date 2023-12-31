import styled from "styled-components";


// ===== ContactForm, newAddressForm, EditAddressForm, CreateAccount ====
export const SubmitInputButton = styled.input`
    background-color: rgba(40,44,52, 1);
    color: whitesmoke;
    padding: 12px 24px;
    border: none;
    letter-spacing: 0.1rem;
    cursor: pointer;
    transition: .3s ease;
    margin: 2rem 0 2rem;
    //border-radius: 4px;
    width: 100%;
  
    //border-radius: 4px;
    //width: 100%;
    &:hover {
      box-shadow: rgba(0, 0, 0, 0.16) 0px 1px 2px, rgb(51, 51, 51) 0px 0px 0px 2px;
    }
`

// ==== ContactForm, NewAddress, EditAddressForm =====
export const CancelButton = styled.button`
    background: none;
    color: rgb(82, 82, 82);
    padding: 12px 24px;
    border: solid 0.5px #282c34;
    letter-spacing: 0.1rem;
    transition: .3s ease;
    cursor: pointer;
    transition: .3s ease;
    margin: 2rem 0;
    //border-radius: 4px;
    box-sizing: border-box;
    
    &:hover {
      box-shadow: rgba(0, 0, 0, 0.16) 0px 1px 2px, rgb(51, 51, 51) 0px 0px 0px 2px;
    }
`

// ===== AddressesPage(add new)
export const DarkButton = styled.button`
    background-color: rgba(40,44,52, 1);
    color: whitesmoke;
    padding: 12px 24px;
    border: none;
    letter-spacing: 0.1rem;
    cursor: pointer;
    transition: .3s ease;
    margin: 2rem 0;
    &:hover {
      box-shadow: rgba(0, 0, 0, 0.16) 0px 1px 2px, rgb(51, 51, 51) 0px 0px 0px 2px;
    }
`

// ======== address (edit/delete) ========================
export const LightButton = styled.button`
    background: none;
    color: rgb(82, 82, 82);
    padding: 12px 24px;
    border: solid 0.5px #282c34;
    letter-spacing: 0.1rem;
    transition: .3s ease;
    cursor: pointer;
    transition: .3s ease;
    margin: 2rem 0;
    box-sizing: border-box;
    
    &:hover {
      box-shadow: rgba(0, 0, 0, 0.16) 0px 1px 2px, rgb(51, 51, 51) 0px 0px 0px 2px;
    }
`

// ====== category(homepage) ===============
export const ShopButtonLink = styled.a`
    color: white;
    background-color: rgba(40,44,52, 0.6);
    width: 136px;
    display: inline-block;
    padding: 12px 0;
    margin: 0 auto;
    cursor: pointer;
    font-size: 0.9rem;
    text-align: center;
    text-decoration: none;
  
    
    &:hover{
      background-color: rgba(40,44,52, 0.9);
    }
`