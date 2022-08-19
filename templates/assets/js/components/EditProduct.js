import React, { useState } from 'react';
import TagsInput from 'react-tagsinput';
import 'react-tagsinput/react-tagsinput.css';
import Dropzone from 'react-dropzone'

import axios from "axios";
import { useParams, useNavigate } from "react-router-dom";

const EditProduct = (props) => {
    const { productID } = useParams();
    // const productID = props.id
    // const navigate = useNavigate()
    const initial_values = { title: "", sku: "", description: "", productimage_set: [], productvariantprice_set: [] };
    const [formData, updateFormData] = useState(initial_values);

    // console.log('first variant id: ', props.variants[0].id)
    const [productVariants, setProductVariant] = useState([
        {
            // option: props.variants[0].id,
            option: 1,
            tags: []
        }
    ])

    // handle click event of the Add button
    const handleAddClick = () => {
        let all_variants = JSON.parse(props.variants.replaceAll("'", '"')).map(el => el.id)
        let selected_variants = productVariants.map(el => el.option);
        let available_variants = all_variants.filter(entry1 => !selected_variants.some(entry2 => entry1 == entry2))
        setProductVariant([...productVariants, {
            option: available_variants[0],
            tags: []
        }])
    };

    // handle input change on tag input
    const handleInputTagOnChange = (value, index) => {
        let product_variants = [...productVariants]
        product_variants[index].tags = value
        setProductVariant(product_variants)

        checkVariant()
    }

    // remove product variant
    const removeProductVariant = (index) => {
        let product_variants = [...productVariants]
        product_variants.splice(index, 1)
        setProductVariant(product_variants)

    }

    // check the variant and render all the combination
    const checkVariant = () => {
        let tags = [];

        productVariants.filter((item) => {
            tags.push(item.tags)
        })

        setProductVariantPrices([])

        getCombn(tags).forEach(item => {
            setProductVariantPrices(productVariantPrice => [...productVariantPrice, {
                title: item,
                price: 0,
                stock: 0
            }])
        })

    }

    // combination algorithm
    function getCombn(arr, pre) {
        pre = pre || '';
        if (!arr.length) {
            return pre;
        }
        let ans = arr[0].reduce(function (ans, value) {
            return ans.concat(getCombn(arr.slice(1), pre + value + '/'));
        }, []);
        return ans;
    }

    // const handleChange = (e) => {
    //     const { name, value } = e.target;
    //     setFormValues({ ...formValues, [name]: value });
    // };

    const refreshPage = () => {
        window.location.reload();
    }

    const handleVariantOnChange = (e) => {
        console.log('selected variant', e.target)
    }

    // dynamic price 
    const handleInputPriceOnChange = (value, index) => {
        let old_productVariantPrices = [...productVariantPrices]
        let ttl = productVariantPrices[index].title
        let stk = productVariantPrices[index].stock
        let new_value = {
            title: ttl,
            price: value,
            stock: stk
        }
        old_productVariantPrices.splice(index, 1, new_value)
        setProductVariantPrices(old_productVariantPrices)
    }

    // dynamic stock
    const handleInputStockOnChange = (value, index) => {
        let old_productVariantPrices = [...productVariantPrices]
        let ttl = productVariantPrices[index].title
        let prc = productVariantPrices[index].price
        let new_value = {
            title: ttl,
            price: prc,
            stock: value
        }
        old_productVariantPrices.splice(index, 1, new_value)
        setProductVariantPrices(old_productVariantPrices)
    }

    const handleChange = (e) => {
        console.log(e.target.name, e.target.value);
        updateFormData({
            ...formData,
            // Trimming any whitespace
            // [e.target.name]: e.target.value.trim(),
            [e.target.name]: e.target.value,
        });
    };

    const cancel = () => {
        // navigate('/')
    }

    const updateProduct = (e) => {
        e.preventDefault();
        console.log(formData);

        axios
            .put(`http://127.0.0.1:8000/product/api/edit/${productID}/`, {
                title: formData.title,
                sku: formData.sku,
                description: formData.description,
                productimage_set: formData.productimage_set,
                productvariantprice_set: formData.productvariantprice_set,
            })
            .then(res => {
                console.log('updated success', res)
                // navigate('/')  // redirect to home page
            })
            .catch(err => console.log(err));
    };

    useEffect(() => {
        // refreshPage()
        axios
            .get(`http://127.0.0.1:8000/product/api/edit/${productID}/`)
            .then(res => {
                console.log('success', res)
                console.log('Title=> ', res.data.productvariantprice_set)
                updateFormData({
                    ...formData,
                    ['title']: res.data.title,
                    ['sku']: res.data.sku,
                    ['description']: res.data.description,
                    ['productimage_set']: res.data.productimage_set,
                    ['productvariantprice_set']: res.data.productvariantprice_set,
                });
            })
            .catch(err => console.log(err));
    }, [updateFormData]);

    return (
        <div>
            <section>
                <div className="row">
                    <div className="col-md-6">
                        <div className="card shadow mb-4">
                            <div className="card-body">
                                <div className="form-group">
                                    <label htmlFor="">Product Name-edited</label>
                                    <input
                                        name='title'
                                        type="text"
                                        placeholder="Product Name"
                                        className="form-control"
                                        value={formData.title}
                                        onChange={handleChange}
                                    />
                                </div>

                                <div className="form-group">
                                    <label htmlFor="">Product SKU</label>
                                    <input
                                        name='sku'
                                        type="text"
                                        placeholder="Product SKU"
                                        className="form-control"
                                        value={formData.sku}
                                        onChange={handleChange} />
                                </div>
                                <div className="form-group">
                                    <label htmlFor="">Description</label>
                                    <textarea
                                        name='description'
                                        id=""
                                        cols="30"
                                        rows="4"
                                        className="form-control"
                                        value={formData.description}
                                        onChange={handleChange}></textarea>
                                </div>
                            </div>
                        </div>

                        <div className="card shadow mb-4">
                            <div
                                className="card-header py-3 d-flex flex-row align-items-center justify-content-between">
                                <h6 className="m-0 font-weight-bold text-primary">Media</h6>
                            </div>
                            <div className="card-body border">
                                <Dropzone onDrop={acceptedFiles => console.log('from create: ', acceptedFiles)}>
                                    {({ getRootProps, getInputProps }) => (
                                        <section>
                                            <div {...getRootProps()}>
                                                <input {...getInputProps()} />
                                                <p>Drag 'n' drop some files here, or click to select files</p>
                                            </div>
                                        </section>
                                    )}
                                </Dropzone>
                            </div>
                        </div>
                    </div>

                    <div className="col-md-6">
                        <div className="card shadow mb-4">
                            <div
                                className="card-header py-3 d-flex flex-row align-items-center justify-content-between">
                                <h6 className="m-0 font-weight-bold text-primary">Variants</h6>
                            </div>
                            <div className="card-body">

                                {
                                    productVariants.map((element, index) => {
                                        return (
                                            <div className="row" key={index}>
                                                <div className="col-md-4">
                                                    <div className="form-group">
                                                        <label htmlFor="">Option</label>
                                                        <select className="form-control" defaultValue={element.option}>
                                                            {
                                                                JSON.parse(props.variants.replaceAll("'", '"')).map((variant, index) => {
                                                                    return (
                                                                        <option key={index} value={variant.id}>{variant.title}</option>)
                                                                })
                                                            }

                                                        </select>
                                                    </div>
                                                </div>

                                                <div className="col-md-8">
                                                    <div className="form-group">
                                                        {
                                                            productVariants.length > 1
                                                                ? <label htmlFor="" className="float-right text-primary"
                                                                    style={{ marginTop: "-30px" }}
                                                                    onClick={() => removeProductVariant(index)}>remove</label>
                                                                : ''
                                                        }

                                                        <section style={{ marginTop: "30px" }}>
                                                            <TagsInput value={element.tags}
                                                                style="margin-top:30px"
                                                                onChange={(value) => handleInputTagOnChange(value, index)} />
                                                        </section>

                                                    </div>
                                                </div>
                                            </div>
                                        )
                                    })
                                }


                            </div>
                            <div className="card-footer">
                                {productVariants.length !== 3
                                    ? <button className="btn btn-primary" onClick={handleAddClick}>Add another
                                        option</button>
                                    : ''
                                }

                            </div>

                            <div className="card-header text-uppercase">Preview</div>
                            <div className="card-body">
                                <div className="table-responsive">
                                    <table className="table">
                                        <thead>
                                            <tr>
                                                <td>Variant</td>
                                                <td>Price</td>
                                                <td>Stock</td>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {
                                                productVariantPrices.map((productVariantPrice, index) => {
                                                    return (
                                                        <tr key={index}>
                                                            <td>{productVariantPrice.title}</td>
                                                            {/* <td><input name='price' className="form-control" type="text" /></td>
                                                            <td><input name='stock' className="form-control" type="text" /></td> */}
                                                            <td><input onChange={(e) => handleInputPriceOnChange(e.target.value, index)} name='price' className="form-control" type="text" /></td>
                                                            <td><input onChange={(e) => handleInputStockOnChange(e.target.value, index)} name='stock' className="form-control" type="text" /></td>
                                                        </tr>
                                                    )
                                                })
                                            }
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <button type="button" onClick={updateProduct} className="btn btn-lg btn-primary">Save</button>
                <button type="button" onClick={cancel} className="btn btn-secondary btn-lg ms-4">Cancel</button>
                {/* testing  */}
                {/* <button type="button" className="btn btn-secondary btn-lg ms-3">Test</button>  */}
            </section>
        </div>
    );
};

export default EditProduct;
