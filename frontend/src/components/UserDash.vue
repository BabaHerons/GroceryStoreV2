<script lang="ts">

import API from "../api"

export default {
    beforeMount(){
        this.get_all_products()
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
            }
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
            <div class="d-flex flex-row-reverse w-100">
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
                          <p class="card-text">{{ product.description }}</p>
                          
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
                          <div class="d-flex justify-content-between mt-3">
                              <button class="btn btn-outline-secondary">Add to cart</button>
                              <button class="btn btn-success">Buy Now</button>
                          </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>