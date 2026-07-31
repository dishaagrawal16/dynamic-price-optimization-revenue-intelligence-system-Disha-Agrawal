import Layout from "../components/Layout";
import ProductTable from "../components/products/ProductTable";
import { useState } from "react";
import AddProductModal from "../components/products/AddProductModal";
function Products() {
  const role = localStorage.getItem("role");
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("All");
  const handleAddProduct = () => {
  setSelectedProduct(null);
  setIsModalOpen(true);
};

const handleEditProduct = (product) => {
  setSelectedProduct(product);
  setIsModalOpen(true);
};
  return (
    <Layout title="Products">
      <div className="flex flex-col md:flex-row justify-between gap-4 mb-6">
        <input
         type="text"
         placeholder="Search by Product ID or Category..."
         value={searchTerm}
         onChange={(e) => setSearchTerm(e.target.value)}
         className="border rounded-lg px-4 py-2 w-full md:w-80"
         />

        <div className="flex gap-3">
<select
  value={selectedCategory}
  onChange={(e) => setSelectedCategory(e.target.value)}
  className="border rounded-lg px-4 py-2"
>
  <option value="All">All Categories</option>
  <option value="Electronics">Electronics</option>
  <option value="Fashion">Fashion</option>
  <option value="Groceries">Groceries</option>
  <option value="Home">Home</option>
  <option value="Beauty">Beauty</option>
</select>

{role === "admin" && (
  <button onClick={handleAddProduct}>
    Add Product
  </button>
)}
        </div>
      </div>

      <ProductTable
  onEdit={handleEditProduct}
  searchTerm={searchTerm}
  selectedCategory={selectedCategory}
/>

      <AddProductModal
  isOpen={isModalOpen}
  onClose={() => setIsModalOpen(false)}
  onProductAdded={() => window.location.reload()}
  editProduct={selectedProduct}
/>

    </Layout>
  );
}

export default Products;