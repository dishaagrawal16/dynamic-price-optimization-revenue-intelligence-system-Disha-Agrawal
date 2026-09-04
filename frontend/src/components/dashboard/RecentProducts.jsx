function RecentProducts({ data }) {
  return (
    <div className="bg-white rounded-2xl shadow-md p-6 overflow-x-auto">
      <h2 className="text-xl font-bold mb-4">
        Recent Products
      </h2>

      <table className="w-full">
        <thead>
          <tr className="border-b">
            <th className="text-left py-2">Product ID</th>
            <th className="text-left py-2">Category</th>
            <th className="text-left py-2">Price</th>
            <th className="text-left py-2">Payment</th>
          </tr>
        </thead>

        <tbody>
          {data.map((product) => (
            <tr key={product.product_id} className="border-b">
              <td className="py-2">{product.product_id}</td>
              <td>{product.category}</td>
              <td>₹{product.price}</td>
              <td>{product.payment_method}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default RecentProducts;