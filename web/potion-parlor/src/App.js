import React, { useState } from 'react';
import axios from 'axios';
import { Button, Dropdown, Input, List, Container, Header, Icon } from 'semantic-ui-react';

const App = () => {
    const [cart, setCart] = useState([]);
    const [selectedPotion, setSelectedPotion] = useState('');
    const [quantity, setQuantity] = useState(1);

    const potions = ['Invisibility', 'Flying', 'Healing', 'Strength', 'Intelligence']
        .map(potion => ({ key: potion, text: potion, value: potion }));

    const addToCart = () => {
        if (selectedPotion === '' || quantity == 0) return;
        const newOrder = { potion: selectedPotion, quantity };
        setCart(prevCart => [...prevCart, newOrder]);
        setSelectedPotion('');
        setQuantity(1);
    };

    const sendOrder = async () => {
        const orderJSON = JSON.stringify(cart);

        try {
            console.log('Sending order...');
            console.log(orderJSON);
            const response = await axios.post('http://localhost:3001/order', orderJSON);
            console.log(response.data);
            setCart([]);
        } catch (error) {
            console.error(error);
        }
    };

    return (
        <Container text>
            <div style={{ color: "white", backgroundColor: "black", padding: "1ex", fontSize: "18pt" }}>
                <Icon name="flask" />Feel the Magic!
                <span style={{ float: "right", }}>
                    Potion Parlor<Icon name="flask" />
                </span>
            </div>
            <Header as='h1'>Order Form</Header>
            <Dropdown
                placeholder='Select Potion'
                fluid
                selection
                options={potions}
                value={selectedPotion}
                onChange={(e, data) => setSelectedPotion(data.value)}
            />

            <Input
                type='number'
                min='1'
                placeholder='Quantity'
                value={quantity}
                onChange={e => setQuantity(e.target.value)}
            />

            <Button primary onClick={addToCart}>Add to Cart</Button>

            <Header as='h2'>Shopping Cart</Header>
            <List>
                {cart.map((item, index) => (
                    <List.Item key={index}>
                        {item.quantity}x {item.potion}
                    </List.Item>
                ))}
            </List>

            <Button secondary onClick={sendOrder}>Send Order</Button>
        </Container>
    );
};

export default App;
