import {useContext, useEffect, useState} from "react";
import {UserContext} from "../../global/user-context/UserContext";
import {DarkButton} from "../../components/buttons";
import {NewAddress} from "./NewAddress";
import {client, fetchFromAPI} from "../../helper-functions/fetchFromAPI";
import {Address} from "./Address";
import {DeleteAddressConfirmation} from "./DeleteAddressConfirmation";
import {LogoutText} from "../../account/AccountPage";
import styled from "styled-components";
import {useNavigate} from "react-router-dom";

export function AddressesPage() {

    const [editingAddressId, setEditingAddressId] = useState(null)

    const [deletingAddressId, setDeletingAddressId] = useState(null)
    const [showDeletePopup, setDeletePopup] = useState(false)

    const [isNewAddress, setNewAddress] = useState(false)
    const [addresses, setAddresses] = useState([])

    const { currentUser, isMobile } = useContext(UserContext)


    useEffect(() => {
        fetchFromAPI('/addresses/', setAddresses)
    }, []);

    function handleNewAddressClick() {
        setNewAddress(!isNewAddress)
        setEditingAddressId(null)
    }

    function onAddNewAddress(newAddress) {
        if (newAddress.is_default) {
            const defaultAddress = addresses.find(address => address.is_default)
            if (defaultAddress) {
                defaultAddress.is_default = false
            }
            setAddresses(prev => [newAddress, ...prev])
        } else {
            setAddresses(prev => [...prev, newAddress])
        }

        setNewAddress(false)
    }

    // =================================== update address ====================================
    function handleEditAddressClick(id) {
        if (editingAddressId === id) {
            setEditingAddressId(null)
        } else {
            setEditingAddressId(id)
        }
        setNewAddress(false)
    }

    function onUpdateAddress(updatedAddress) {
        const updatedAddresses = addresses?.map(address => {
            if (address.id === updatedAddress.id) {
                return {...address, is_default: true};
            } else {
                return {...address, is_default: false};
            }
        })

        // Sort the addresses to ensure the `is_default` address is at the top
        updatedAddresses.sort((a, b) => b.is_default - a.is_default);

        setAddresses(updatedAddresses)
    }

    // =================================== delete address ====================================
    function handleDeleteAddressClick(e) {
        const id = parseInt(e.target.value)
        setDeletePopup(true)
        setDeletingAddressId(id)
    }

    function handleDeleteAddress() {
        // const id = parseInt(e.target.value)
        client.delete(`/address/${deletingAddressId}/`, {withCredentials: true})
            .then(res => {
                onDeleteAddress(deletingAddressId)
            })
            .catch(error => console.log(error.response.data))
        setDeletePopup(null)
    }
    function onDeleteAddress(deleteId) {
        const updatedAddresses = addresses?.filter(address => {
            return address.id !== deleteId
        })
        setAddresses(updatedAddresses)
    }


    // ====================================================================
    const navigate = useNavigate()

    function handleBackToAccoutnPage() {
        navigate('/account/')
    }

    return (
        <>
            {showDeletePopup && (
                <DeleteAddressConfirmation
                    setDeletePopup={setDeletePopup}
                    handleDeleteAddress={handleDeleteAddress}
                />
            )}

            <div
                style={{
                    margin: isMobile ? "0 16px" : "0 auto",
                }}
            >
                <div style={{
                    padding: "60px 0 35px",
                    // borderBottom: "1px solid #dddddd"
                }}>
                    <h1>Addresses</h1>
                    <BackToAccount onClick={handleBackToAccoutnPage}>
                        Back to account
                    </BackToAccount>
                </div>

                <section>
                    <div>

                        <DarkButton onClick={handleNewAddressClick}>
                            Add New Address
                        </DarkButton>

                        {isNewAddress && (
                            <NewAddress
                                setNewAddress={setNewAddress}
                                onAddNewAddress={onAddNewAddress}
                                setAddresses={{setAddresses}}
                            />
                        )}

                        <ul style={{paddingLeft: "0", listStyle: "none"}}>
                            {addresses?.map((address, index) => {
                                return (
                                    <Address
                                        key={`${currentUser?.first_name}-${index}`}
                                        address={address}
                                        isEditAddress={editingAddressId === address.id}
                                        handleEditAddressClick={() => handleEditAddressClick(address.id)}
                                        setEditingAddressId={setEditingAddressId}
                                        onUpdateAddress={onUpdateAddress}

                                        handleDeleteAddressClick={handleDeleteAddressClick}
                                    />
                            )})}
                        </ul>

                    </div>
                </section>


            </div>
        </>
    )
}


const BackToAccount = styled(LogoutText)``