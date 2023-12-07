<script lang="ts">

import API from "../api"

export default {
    beforeMount(){
        this.get_all_products()
        this.get_cart()
    },
    mounted() {
        let source = new EventSource("http://localhost:5000/stream")
        // SSE FOR NEW PRODUCT ADDED
        source.addEventListener("product", (event:any) => {
            const data = JSON.parse(event.data)
            if (data.message.includes("out of stock")){
                this.sse.red.push(data.message)
            } else {
                this.sse.green.push(data.message)
            }
            this.get_all_products()
        })
    },
    data: () => {
        return {
            product_list:[] as any[],
            category:[] as any[],
            sse:{
                green:[] as any[],
                red:[] as any[]
            },
            cart:[] as any[],
            cart_total:0
        }
    },
    methods: {
        get_all_products(){
            API.get_all_products()
            .then(response => response.json())
            .then(data => {
                let k = data
                this.product_list = k
                
                // POPULATING ALL AVAILABLE CATEGORIES
                for (let i=0; i<this.product_list.length; i++){
                    let cat = this.product_list[i].category
                    if (this.category.includes(cat)){}
                    else {
                        this.category.push(cat)
                    }
                }
            })
        },
        get_cart(){
            API.get_cart()
            .then(response => response.json())
            .then(data => {
                this.cart = data
                this.cart_total = 0
                for (let i=0; i<this.cart.length; i++){
                    this.cart[i].item_total = this.cart[i].quantity * Number(this.cart[i].price)
                    this.cart_total += this.cart[i].item_total
                }
            })
        },
        add_to_cart(product_id:any){
            let json_data = {
                "product_id": product_id,
                "user_id": `${localStorage.getItem("user_id")}`,
                "quantity": 1
            }
            API.post_cart(json_data)
            .then(response => response.json())
            .then(data => {
                console.log(data);
                alert("Product added to cart.")
                this.get_cart()
            })
        },
        item_total(cart_id:any){
            for (let i=0; i<this.cart.length; i++){
                if (this.cart[i].id == cart_id){
                    this.cart[i].item_total = Number(this.cart[i].quantity) * Number(this.cart[i].price)
                    
                    let json_data = {"quantity":this.cart[i].quantity}
                    API.patch_cart(json_data, cart_id)
                    .then(response => response.json())
                    .then(data => {
                        console.log(data);
                        this.get_cart()
                    })
                    break
                }
            }
        },
        remove_from_cart(cart_id:any, product_name:any){
            if(confirm(`Are you sure you want to remove item: "${product_name}" from cart?`)){
                API.delete_item_from_cart(cart_id)
                .then(Response => Response.json())
                .then(data => {
                    console.log(data)
                    this.get_cart()
                })
            }
        },
        buy_now(){
            if (confirm("Do you want to purchase all items in your cart?")){
                let json_data = {
                    "products": JSON.stringify(this.cart),
                    "amount":this.cart_total
                }
                API.post_order(json_data)
                .then(Response => Response.json())
                .then(data => {
                    console.log(data);
                    this.get_cart()
                    this.get_all_products()
                })
            }
        },
    }
}
</script>

<template>
    <div class="container pb-2 ">
        <!-- SEARCH BAR -->
        <div class="d-flex align-items-center justify-content-center mt-4">
            <input type="text" class="form-control" placeholder="Search products here">
            <button class="btn btn-secondary fw-bold ">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-search" viewBox="0 0 16 16">
                    <path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0"/>
                </svg>
            </button>
            <div class="d-flex flex-row-reverse w-100" data-bs-toggle="modal" data-bs-target="#cartModal">
                <button class="btn btn-secondary">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-cart3" viewBox="0 0 16 16">
                        <path d="M0 1.5A.5.5 0 0 1 .5 1H2a.5.5 0 0 1 .485.379L2.89 3H14.5a.5.5 0 0 1 .49.598l-1 5a.5.5 0 0 1-.465.401l-9.397.472L4.415 11H13a.5.5 0 0 1 0 1H4a.5.5 0 0 1-.491-.408L2.01 3.607 1.61 2H.5a.5.5 0 0 1-.5-.5M3.102 4l.84 4.479 9.144-.459L13.89 4H3.102zM5 12a2 2 0 1 0 0 4 2 2 0 0 0 0-4m7 0a2 2 0 1 0 0 4 2 2 0 0 0 0-4m-7 1a1 1 0 1 1 0 2 1 1 0 0 1 0-2m7 0a1 1 0 1 1 0 2 1 1 0 0 1 0-2"/>
                    </svg>
                </button>
            </div>
        </div>

        <!-- FOR DISPLAYING ANY NOTIFICATION -->
        <div class="mt-4">
            <div v-for="msg in sse.red" class="alert alert-danger alert-dismissible fade show" role="alert">
                <strong>{{ msg }}</strong>
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
            <div v-for="msg in sse.green" class="alert alert-success alert-dismissible fade show" role="alert">
                <strong>{{ msg }}</strong>
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
        </div>

        <!-- LIST OF ALL PRODUCTS WITH RESPECTIVE CATEGORY -->
        <div v-for="cat in category" class="mt-4">
            <div class="d-flex justify-content-between border-bottom border-black">
                <h2 class="text-secondary">{{ cat }}</h2>
            </div>
            <div class="d-flex flex-wrap justify-content-center">
                <div v-for="product in product_list">
                    <div  v-if="product.category == cat" class="card m-4 shadow" style="width: 18rem;">
                        <!-- <img src="..." class="card-img-top" alt="..."> -->
                        <div class="card-body">
                            <!-- PRODUCT NAME -->
                          <h5 class="card-title">{{ product.name }}</h5>
                          
                          <!-- PRODUCT DESCRIPTION -->
                          <p class="card-text" style="overflow-y: auto; height: 100px;">{{ product.description }}</p>
                          
                          <!-- PRICE & STOCK DETAILS -->
                          <div class="mb-2 fw-semibold d-flex justify-content-between ">
                            <div>
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-currency-rupee" viewBox="0 0 16 16">
                                    <path d="M4 3.06h2.726c1.22 0 2.12.575 2.325 1.724H4v1.051h5.051C8.855 7.001 8 7.558 6.788 7.558H4v1.317L8.437 14h2.11L6.095 8.884h.855c2.316-.018 3.465-1.476 3.688-3.049H12V4.784h-1.345c-.08-.778-.357-1.335-.793-1.732H12V2H4z"/>
                                </svg>
                                <span>{{ product.price }} / {{ product.unit }}</span>
                            </div>
                            <span v-if="product.stock > 0" class="badge text-bg-info">In Stock</span>
                            <span v-else class="badge text-bg-danger">Out of Stock</span>
                          </div>

                          <!-- MANUFACTURE & EXPIRY DATES -->
                          <div v-if="product.stock > 0" class="d-flex justify-content-between mt-4">
                            <div>
                                <span class="border-bottom border-black">Mfg. Date</span> <br>
                                <span class="text-success">{{ product.m_date }}</span>
                            </div>
                            <div>
                                <span class="border-bottom border-black">Exp. Date</span> <br>
                                <span class="text-danger">{{ product.e_date }}</span>
                            </div>
                          </div>

                          <!-- ADD TO CART & BUY NOW BUTTONS -->
                          <div v-if="product.stock > 0" class="d-flex justify-content-between mt-3">
                              <button v-on:click="add_to_cart(product.id)" class="btn btn-outline-secondary">Add to cart</button>
                              <button class="btn btn-success">Buy Now</button>
                          </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- CART MODAL -->
        <div class="modal fade" id="cartModal" tabindex="-1" aria-labelledby="registerLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-scrollable">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" id="registerLabel">Cart</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <div v-if="cart.length > 0" class="d-flex flex-wrap justify-content-center">
                        <div v-for="product in cart">
                            <div class="card m-2 shadow-sm" style="width: 18rem;">
                                <!-- <img src="..." class="card-img-top" alt="..."> -->
                                <div class="card-body">
                                  <!-- PRODUCT NAME -->
                                  <span class="text-secondary">{{ product.category }}</span>
                                  <h5 class="card-title">{{ product.name }}</h5>
                                  <span>{{ product.product_id }}</span>

                                  <!-- PRICE & QUANTITY DETAILS -->
                                  <div class="mt-2 mb-2 fw-semibold d-flex justify-content-between ">
                                    <!-- PRICE OF PRODUCT -->
                                    <div>
                                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-currency-rupee" viewBox="0 0 16 16">
                                            <path d="M4 3.06h2.726c1.22 0 2.12.575 2.325 1.724H4v1.051h5.051C8.855 7.001 8 7.558 6.788 7.558H4v1.317L8.437 14h2.11L6.095 8.884h.855c2.316-.018 3.465-1.476 3.688-3.049H12V4.784h-1.345c-.08-.778-.357-1.335-.793-1.732H12V2H4z"/>
                                        </svg>
                                        <span>{{ product.price }} / {{ product.unit }}</span>
                                    </div>
                                    <div>
                                        <label for="quantity">Quantity</label> &nbsp;
                                        <input style="width: 60px;" type="number" v-on:change="item_total(product.id)" v-model="product.quantity" name="quantity" id="quantity">
                                    </div>
                                  </div>
                                
                                  <!-- ITEM TOTAL & DELETE BUTTON -->
                                  <div class="d-flex justify-content-between fw-semibold mt-4">
                                    <div class="text-primary">
                                        <span>Total:</span>
                                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-currency-rupee" viewBox="0 0 16 16">
                                            <path d="M4 3.06h2.726c1.22 0 2.12.575 2.325 1.724H4v1.051h5.051C8.855 7.001 8 7.558 6.788 7.558H4v1.317L8.437 14h2.11L6.095 8.884h.855c2.316-.018 3.465-1.476 3.688-3.049H12V4.784h-1.345c-.08-.778-.357-1.335-.793-1.732H12V2H4z"/>
                                        </svg>
                                        <span>{{ product.item_total }}</span>
                                    </div>
                                    <!-- DELETE FROM CART BUTTON -->
                                    <button v-on:click="remove_from_cart(product.id, product.name)" class="btn btn-danger">
                                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash" viewBox="0 0 16 16">
                                            <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0z"/>
                                            <path d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4zM2.5 3h11V2h-11z"/>
                                        </svg>
                                    </button>
                                  </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="text-center fw-semibold" v-else>Cart is empty.</div>
                </div>
                <div v-if="cart.length > 0" class="modal-footer d-flex flex-row-reverse justify-content-between ">
                    <button v-on:click="buy_now" type="button" class="btn btn-success" data-bs-dismiss="modal">Buy Now</button>
                    <p>
                        <span>Cart Total: </span>
                        <span class="fw-bold text-primary">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-currency-rupee" viewBox="0 0 16 16">
                                <path d="M4 3.06h2.726c1.22 0 2.12.575 2.325 1.724H4v1.051h5.051C8.855 7.001 8 7.558 6.788 7.558H4v1.317L8.437 14h2.11L6.095 8.884h.855c2.316-.018 3.465-1.476 3.688-3.049H12V4.784h-1.345c-.08-.778-.357-1.335-.793-1.732H12V2H4z"/>
                            </svg>{{ cart_total }}
                        </span>
                    </p>
                </div>
            </div>
            </div>
        </div>
    </div>
</template>