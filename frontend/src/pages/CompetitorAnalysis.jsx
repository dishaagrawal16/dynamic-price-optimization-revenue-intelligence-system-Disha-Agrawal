import { useEffect, useMemo, useState } from "react";

import {
  getCompetitorSummary,
  getCompetitorComparison,
  getCompetitorProducts,
  getCategoryCompetitorPrices,
  getMarketIntelligence,
} from "../services/dashboardService";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
  ReferenceLine
} from "recharts";


function CompetitorAnalysis() {

  const [summary, setSummary] = useState(null);
  const [comparison, setComparison] = useState([]);
  const [products, setProducts] = useState([]);
  const [categoryPrices, setCategoryPrices] = useState([]);
  const [marketIntelligence, setMarketIntelligence] = useState([]);

  const [selectedCategory, setSelectedCategory] = useState("All");
  const [selectedCompetitor, setSelectedCompetitor] = useState("All");

  const [loading, setLoading] = useState(true);


  // ============================================================
  // FETCH DATA
  // ============================================================

  useEffect(() => {

    const fetchData = async () => {

      try {

        const [
          summaryData,
          comparisonData,
          productsData,
          categoryPricesData,
          marketIntelligenceData
        ] = await Promise.all([

          getCompetitorSummary(),

          getCompetitorComparison(),

          getCompetitorProducts(),

          getCategoryCompetitorPrices(),
          getMarketIntelligence(),
        ]);


        setSummary(summaryData);

        setComparison(comparisonData);

        setProducts(productsData);

        setCategoryPrices(categoryPricesData);

        setMarketIntelligence(
           marketIntelligenceData
        );
      } catch (error) {

        console.error(
          "Error loading competitor analysis:",
          error
        );

        console.error(
          "Response:",
          error.response?.data
        );

      } finally {

        setLoading(false);

      }

    };


    fetchData();

  }, []);


  // ============================================================
  // FILTER OPTIONS
  // ============================================================

  const categories = useMemo(() => {

    return [
      "All",
      ...new Set(
        products
          .map((item) => item.Category)
          .filter(Boolean)
      ),
    ];

  }, [products]);


  const competitors = useMemo(() => {

    return [
      "All",
      ...new Set(
        products
          .map((item) => item.Competitor)
          .filter(Boolean)
      ),
    ];

  }, [products]);


  // ============================================================
  // FILTER PRODUCTS
  // ============================================================

  const filteredProducts = useMemo(() => {

    return products.filter((product) => {

      const categoryMatch =
        selectedCategory === "All" ||
        product.Category === selectedCategory;

      const competitorMatch =
        selectedCompetitor === "All" ||
        product.Competitor === selectedCompetitor;

      return (
        categoryMatch &&
        competitorMatch
      );

    });

  }, [
    products,
    selectedCategory,
    selectedCompetitor,
  ]);


  // ============================================================
// PRICE GAP CHART DATA
// Only use categories with valid comparable competitor pricing
// ============================================================

const priceGapData = useMemo(() => {

  return comparison
    .filter((item) => {

      const gap = Number(item.Price_Gap_Percent);

      return (
        item.Market_Position !== "Insufficient Comparable Data" &&
        Number.isFinite(gap)
      );

    })
    .map((item) => ({
      Category: item.Category,
      Price_Gap_Percent: Number(
        item.Price_Gap_Percent
      )
    }));

}, [comparison]);
  // ============================================================
  // LOADING
  // ============================================================

  if (loading) {

    return (

      <div className="p-6">

        <p className="text-gray-600">

          Loading competitor analysis...

        </p>

      </div>

    );

  }


  // ============================================================
  // FORMAT PRICE
  // ============================================================

  const formatPrice = (value) => {

    if (
      value === null ||
      value === undefined ||
      isNaN(Number(value))
    ) {

      return "—";

    }

    return `₹${Number(value).toLocaleString(
      "en-IN",
      {
        maximumFractionDigits: 2,
      }
    )}`;

  };


  // ============================================================
  // MAIN UI
  // ============================================================

  return (

    <div className="p-6 space-y-6">


      {/* ====================================================== */}
      {/* HEADER */}
      {/* ====================================================== */}

      <div>

        <h1 className="text-3xl font-bold text-gray-800">

          Competitor Analysis

        </h1>

        <p className="text-gray-500 mt-1">

          Monitor competitor pricing, discounts and market position.

        </p>

      </div>


      {/* ====================================================== */}
      {/* SUMMARY CARDS */}
      {/* ====================================================== */}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">


        {/* Products */}

        <div className="bg-white rounded-2xl shadow-md p-5">

          <p className="text-gray-500 text-sm">

            Products Monitored

          </p>

          <h2 className="text-3xl font-bold mt-2 text-blue-600">

            {summary?.total_products ?? 0}

          </h2>

          <p className="text-xs text-gray-400 mt-2">

            Live competitor observations

          </p>

        </div>


        {/* Competitors */}

        <div className="bg-white rounded-2xl shadow-md p-5">

          <p className="text-gray-500 text-sm">

            Competitors

          </p>

          <h2 className="text-3xl font-bold mt-2 text-orange-500">

            {summary?.competitors_monitored ?? 0}

          </h2>

          <p className="text-xs text-gray-400 mt-2">

            Market sources monitored

          </p>

        </div>


        {/* Categories */}

        <div className="bg-white rounded-2xl shadow-md p-5">

          <p className="text-gray-500 text-sm">

            Categories Covered

          </p>

          <h2 className="text-3xl font-bold mt-2 text-green-600">

            {summary?.categories_covered ?? 0}

          </h2>

          <p className="text-xs text-gray-400 mt-2">

            Product categories

          </p>

        </div>


        {/* Average */}

        <div className="bg-white rounded-2xl shadow-md p-5">

          <p className="text-gray-500 text-sm">

            Avg Competitor Price

          </p>

          <h2 className="text-3xl font-bold mt-2">

            {formatPrice(
              summary?.average_competitor_price
            )}

          </h2>

          <p className="text-xs text-gray-400 mt-2">

            Across monitored products

          </p>

        </div>

      </div>


      {/* ====================================================== */}
      {/* CATEGORY / COMPETITOR OVERVIEW */}
      {/* ====================================================== */}

      <div className="bg-white rounded-2xl shadow-md p-6">

        <div className="flex justify-between items-center mb-5">

          <div>

            <h2 className="text-xl font-bold">

              Competitor Market Overview

            </h2>

            <p className="text-sm text-gray-500">

              Category-wise competitor pricing statistics

            </p>

          </div>

        </div>


        <div className="overflow-x-auto">

          <table className="w-full text-left">

            <thead>

              <tr className="border-b text-gray-500 text-sm">

                <th className="py-3">
                  Category
                </th>

                <th>
                  Competitor
                </th>

                <th>
                  Products
                </th>

                <th>
                  Avg Price
                </th>

                <th>
                  Min Price
                </th>

                <th>
                  Max Price
                </th>

                <th>
                  Avg Discount
                </th>

              </tr>

            </thead>


            <tbody>

              {categoryPrices.map(
                (item, index) => (

                  <tr
                    key={index}
                    className="border-b hover:bg-gray-50"
                  >

                    <td className="py-3 font-medium">

                      {item.Category}

                    </td>

                    <td>

                      <span className="px-3 py-1 rounded-full bg-blue-50 text-blue-700 text-sm">

                        {item.Competitor}

                      </span>

                    </td>

                    <td>

                      {item.Product_Count}

                    </td>

                    <td className="font-medium">

                      {formatPrice(
                        item.Average_Price
                      )}

                    </td>

                    <td>

                      {formatPrice(
                        item.Minimum_Price
                      )}

                    </td>

                    <td>

                      {formatPrice(
                        item.Maximum_Price
                      )}

                    </td>

                    <td>

                      {item.Average_Discount !== null &&
                      item.Average_Discount !== undefined
                        ? `${Number(
                            item.Average_Discount
                          ).toFixed(2)}%`
                        : "—"}

                    </td>

                  </tr>

                )
              )}

            </tbody>

          </table>

        </div>

      </div>


{/* ====================================================== */}
{/* PRICE GAP BY CATEGORY */}
{/* ====================================================== */}

<div className="bg-white rounded-2xl shadow-md p-6">

  <div className="mb-5">

    <h2 className="text-xl font-bold text-gray-800">
      Price Gap vs Competitors
    </h2>

    <p className="text-sm text-gray-500 mt-1">
      Difference between our average price and comparable competitor prices
    </p>

    <p className="text-xs text-gray-400 mt-2">
      Negative values mean our price is lower than the competitor.
      Categories without comparable pricing data are excluded.
    </p>

  </div>

  <ResponsiveContainer
    width="100%"
    height={360}
  >

    <BarChart
      data={priceGapData}
      layout="vertical"
      margin={{
        top: 10,
        right: 30,
        left: 30,
        bottom: 20,
      }}
    >

      <CartesianGrid
        strokeDasharray="3 3"
        horizontal={true}
        vertical={true}
      />

      <XAxis
        type="number"
        domain={[-100, 20]}
        tickFormatter={(value) =>
          `${value}%`
        }
      />

      <YAxis
        type="category"
        dataKey="Category"
        width={100}
      />

      <ReferenceLine
        x={0}
        stroke="#6b7280"
        strokeWidth={2}
      />

      <Tooltip
        formatter={(value) =>
          `${Number(value).toFixed(2)}%`
        }
        labelFormatter={(label) =>
          `Category: ${label}`
        }
      />

      <Bar
        dataKey="Price_Gap_Percent"
        name="Price Gap"
        fill="#2563eb"
        radius={[6, 0, 0, 6]}
        barSize={42}
      />

    </BarChart>

  </ResponsiveContainer>

</div>

{/* ====================================================== */}
{/* MARKET INTELLIGENCE */}
{/* ====================================================== */}

<div className="bg-white rounded-2xl shadow-md p-6">

  <div className="mb-6">

    <h2 className="text-xl font-bold text-gray-800">
      Market Intelligence
    </h2>

    <p className="text-sm text-gray-500 mt-1">
      Category-level competitive pressure, pricing
      opportunities and market insights.
    </p>

  </div>


  {/* ================================================== */}
  {/* INTELLIGENCE CARDS */}
  {/* ================================================== */}

  <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">

    <div className="bg-red-50 rounded-xl p-4">

      <p className="text-sm text-gray-500">
        High Pressure Categories
      </p>

      <p className="text-2xl font-bold text-red-600 mt-1">

        {
          marketIntelligence.filter(
            (item) =>
              item.Competitive_Pressure === "High"
          ).length
        }

      </p>

    </div>


    <div className="bg-green-50 rounded-xl p-4">

      <p className="text-sm text-gray-500">
        Optimization Opportunities
      </p>

      <p className="text-2xl font-bold text-green-600 mt-1">

        {
          marketIntelligence.filter(
            (item) =>
              item.Market_Opportunity ===
              "Potential price optimization opportunity"
          ).length
        }

      </p>

    </div>


    <div className="bg-blue-50 rounded-xl p-4">

      <p className="text-sm text-gray-500">
        Categories Analyzed
      </p>

      <p className="text-2xl font-bold text-blue-600 mt-1">

        {marketIntelligence.length}

      </p>

    </div>

  </div>


  {/* ================================================== */}
  {/* MARKET INTELLIGENCE TABLE */}
  {/* ================================================== */}

  <div className="overflow-x-auto">

    <table className="w-full text-left">

      <thead>

        <tr className="border-b text-gray-500 text-sm">

          <th className="py-3">
            Category
          </th>

          <th>
            Demand
          </th>

          <th>
            Our Discount
          </th>

          <th>
            Competitor Discount
          </th>

          <th>
            Market Position
          </th>

          <th>
            Pressure
          </th>

          <th>
            Opportunity
          </th>

        </tr>

      </thead>


      <tbody>

        {marketIntelligence.map(
          (item, index) => (

            <tr
              key={index}
              className="border-b hover:bg-gray-50"
            >

              <td className="py-4 font-medium">
                {item.Category_Name}
              </td>


              <td>
                {item.Average_Demand
                  ? Number(
                      item.Average_Demand
                    ).toFixed(2)
                  : "—"}
              </td>


              <td>
                {item.Average_Discount !== null
                  ? `${Number(
                      item.Average_Discount
                    ).toFixed(2)}%`
                  : "—"}
              </td>


              <td>
                {item.Competitor_Average_Discount !== null
                  ? `${Number(
                      item.Competitor_Average_Discount
                    ).toFixed(2)}%`
                  : "—"}
              </td>


              {/* MARKET POSITION */}

              <td>

                <span
                  className={`px-3 py-1 rounded-full text-xs font-medium ${
                    item.Market_Position ===
                    "Below Competitor"
                      ? "bg-yellow-100 text-yellow-700"
                      : item.Market_Position ===
                        "Above Competitor"
                      ? "bg-red-100 text-red-700"
                      : item.Market_Position ===
                        "Competitive"
                      ? "bg-green-100 text-green-700"
                      : "bg-gray-100 text-gray-600"
                  }`}
                >

                  {item.Market_Position}

                </span>

              </td>


              {/* PRESSURE */}

              <td>

                <span
                  className={`px-3 py-1 rounded-full text-xs font-medium ${
                    item.Competitive_Pressure ===
                    "High"
                      ? "bg-red-100 text-red-700"
                      : item.Competitive_Pressure ===
                        "Medium"
                      ? "bg-yellow-100 text-yellow-700"
                      : item.Competitive_Pressure ===
                        "Low"
                      ? "bg-green-100 text-green-700"
                      : "bg-gray-100 text-gray-600"
                  }`}
                >

                  {item.Competitive_Pressure}

                </span>

              </td>


              {/* OPPORTUNITY */}

              <td className="max-w-xs">

                <span className="text-sm text-gray-700">

                  {item.Market_Opportunity}

                </span>

              </td>

            </tr>

          )
        )}

      </tbody>

    </table>

  </div>

</div>

      {/* ====================================================== */}
      {/* PRICING COMPARISON TABLE */}
      {/* ====================================================== */}

      <div className="bg-white rounded-2xl shadow-md p-6">

        <h2 className="text-xl font-bold mb-5">

          Pricing Comparison

        </h2>


        <div className="overflow-x-auto">

          <table className="w-full text-left">

            <thead>

              <tr className="border-b text-gray-500 text-sm">

                <th className="py-3">
                  Category
                </th>

                <th>
                  Competitor
                </th>

                <th>
                  Our Price
                </th>

                <th>
                  Competitor Price
                </th>

                <th>
                  Price Gap
                </th>

                <th>
                  Market Position
                </th>

              </tr>

            </thead>


            <tbody>

              {comparison.map(
                (item, index) => {

                  const gap =
                    Number(
                      item.Price_Gap_Percent
                    );

                  return (

                    <tr
                      key={index}
                      className="border-b hover:bg-gray-50"
                    >

                      <td className="py-3 font-medium">

                        {item.Category}

                      </td>

                      <td>

                        {item.Competitor}

                      </td>

                      <td>

                        {formatPrice(
                          item.Our_Average_Final_Price
                        )}

                      </td>

                      <td>

                        {formatPrice(
                          item.Competitor_Average_Price
                        )}

                      </td>

                      <td>

                        {isNaN(gap)
                          ? "—"
                          : `${gap.toFixed(2)}%`}

                      </td>

                      <td>

                        <span
                          className={`px-3 py-1 rounded-full text-sm ${
                            item.Market_Position ===
                            "Below Competitor"
                              ? "bg-green-100 text-green-700"
                              : item.Market_Position ===
                                "Above Competitor"
                              ? "bg-red-100 text-red-700"
                              : "bg-gray-100 text-gray-700"
                          }`}
                        >

                          {item.Market_Position}

                        </span>

                      </td>

                    </tr>

                  );

                }
              )}

            </tbody>

          </table>

        </div>

      </div>


      {/* ====================================================== */}
      {/* PRODUCT MONITORING */}
      {/* ====================================================== */}

      <div className="bg-white rounded-2xl shadow-md p-6">

        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-5">

          <div>

            <h2 className="text-xl font-bold">

              Monitored Competitor Products

            </h2>

            <p className="text-sm text-gray-500">

              {filteredProducts.length} products shown

            </p>

          </div>


          {/* Filters */}

          <div className="flex gap-3">


            <select
              value={selectedCategory}
              onChange={(e) =>
                setSelectedCategory(
                  e.target.value
                )
              }
              className="border rounded-lg px-3 py-2 text-sm"
            >

              {categories.map(
                (category) => (

                  <option
                    key={category}
                    value={category}
                  >

                    {category}

                  </option>

                )
              )}

            </select>


            <select
              value={selectedCompetitor}
              onChange={(e) =>
                setSelectedCompetitor(
                  e.target.value
                )
              }
              className="border rounded-lg px-3 py-2 text-sm"
            >

              {competitors.map(
                (competitor) => (

                  <option
                    key={competitor}
                    value={competitor}
                  >

                    {competitor}

                  </option>

                )
              )}

            </select>

          </div>

        </div>


        <div className="overflow-x-auto">

          <table className="w-full text-left">

            <thead>

              <tr className="border-b text-gray-500 text-sm">

                <th className="py-3">
                  Competitor
                </th>

                <th>
                  Category
                </th>

                <th>
                  Product
                </th>

                <th>
                  Price
                </th>

                <th>
                  MRP
                </th>

                <th>
                  Discount
                </th>

              </tr>

            </thead>


            <tbody>

              {filteredProducts
                .slice(0, 50)
                .map(
                  (product, index) => {

                    const price =
                      Number(
                        product.Competitor_Price
                      );

                    const mrp =
                      Number(
                        product.MRP
                      );

                    const discount =
                      mrp > 0
                        ? (
                            (
                              mrp - price
                            ) /
                            mrp
                          ) *
                          100
                        : null;

                    return (

                      <tr
                        key={index}
                        className="border-b hover:bg-gray-50"
                      >

                        <td className="py-3">

                          <span className="px-3 py-1 rounded-full bg-blue-50 text-blue-700 text-sm">

                            {product.Competitor}

                          </span>

                        </td>

                        <td>

                          {product.Category}

                        </td>

                        <td className="max-w-md">

                          <div
                            className="truncate"
                            title={
                              product.Product_Name
                            }
                          >

                            {product.Product_Name}

                          </div>

                        </td>

                        <td className="font-medium">

                          {formatPrice(
                            product.Competitor_Price
                          )}

                        </td>

                        <td>

                          {formatPrice(
                            product.MRP
                          )}

                        </td>

                        <td>

                          {discount !== null &&
                          !isNaN(discount)
                            ? `${discount.toFixed(1)}%`
                            : "—"}

                        </td>

                      </tr>

                    );

                  }
                )}

            </tbody>

          </table>

        </div>


        {filteredProducts.length > 50 && (

          <p className="text-sm text-gray-500 mt-4">

            Showing first 50 of{" "}
            {filteredProducts.length}{" "}
            matching products.

          </p>

        )}

      </div>


    </div>

  );

}


export default CompetitorAnalysis;