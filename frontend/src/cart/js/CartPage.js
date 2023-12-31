import {useContext} from "react";
import {UserContext} from "../../global/user-context/UserContext";


import {HeaderText, ModalBody, ModalContainer, ModalFooter, ModalHeader} from "../../components/popupStyles";
import styled from "styled-components";
import '../css/cart-page.css'

import close_black_24dp from "../icons/close_black_24dp.svg"

import {UserCartBody} from "./UserCartBody";
import {UserCartFooter} from "./UserCartFooter";
import {UserAnonymousCartFooter} from "./UserAnonymousCartFooter";
import {UserAnonymousCartBody} from "./UserAnonymousCartBody";
import {OverlayBackground} from "./OverlayBackground";



export function CartPage() {

    const {isLogin, cart, openCart, setOpenCart, isMobile, isTablet} = useContext(UserContext)

    function handleCloseCart() {
        setOpenCart(!openCart)
    }

    return(
        <>
            {openCart && (
                <>


                <ModalContainer style={{zIndex: "9999"}} >
                    {/**/}
                    {!isMobile && !isTablet && (
                        <OverlayBackground action="cart" setAction={setOpenCart}/>
                    )}

                    <CartModalDialog className='cart-page'>
                        <ModalHeader style={{display: "flex", flex: "0 0 auto", alignItems: "center"}}>
                            <HeaderText>Your Cart</HeaderText>
                            <button
                                style={{
                                    border: "none",
                                    background: "none",
                                    position: "absolute",
                                    right: "10px",
                                    cursor: "pointer",
                                }}
                                onClick={handleCloseCart}
                            >
                                <img src={close_black_24dp} alt='close cart'/>
                            </button>
                        </ModalHeader>

                        <ModalBody style={{height: "calc(100% - 200px)", overflowY: "scroll"}}>

                            {isLogin ?
                                <UserCartBody/>
                                :
                                <UserAnonymousCartBody/>
                            }

                        </ModalBody>
                        <ModalFooter>
                            {isLogin ?
                                <UserCartFooter cartItems={cart[0]}/>
                                :
                                <UserAnonymousCartFooter/>
                            }
                        </ModalFooter>

                    </CartModalDialog>
                </ModalContainer>
                </>
            )}
        </>
    )
}

const CartModalDialog = styled.div`
    box-sizing: border-box;
    position: fixed;
    background-color: white;
    top: 0;
    right: 0;
    height: 100%;
    display: flex;
    flex-flow: column nowrap;
    justify-content: flex-start;
    align-items: stretch;

    // slide the cart from right to left
    transform: translateX(100%);
    animation: slideLeft 0.3s ease forwards;
    
    @keyframes slideLeft {
      0% {
        transform: translateX(100%);
      }
      100% {
        transform: translateX(0%);
      }
    }
`