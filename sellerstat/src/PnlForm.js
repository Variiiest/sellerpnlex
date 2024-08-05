import React, { useState } from 'react';
import axios from 'axios';
import './index.css';  // Ensure this CSS file is imported

const PnlForm = () => {
    const [storeId, setStoreId] = useState('');
    const [startDate, setStartDate] = useState('');
    const [endDate, setEndDate] = useState('');
    const [pnlData, setPnlData] = useState(null);
    const [error, setError] = useState(null);

    const handleStoreIdChange = (event) => {
        setStoreId(event.target.value);
    };

    const handleStartDateChange = (event) => {
        setStartDate(event.target.value);
    };

    const handleEndDateChange = (event) => {
        setEndDate(event.target.value);
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        try {
            const response = await axios.get(`http://127.0.0.1:8000/api/pnl/${storeId}/`, {
                params: {
                    start_date: startDate,
                    end_date: endDate,
                },
            });
            setPnlData(response.data);
            setError(null);
        } catch (err) {
            setError(`Error fetching data: ${err.message}`);
            setPnlData(null);
        }
    };

    return (
        <div className="max-w-full mx-auto p-4">
            <h1 className="text-2xl font-bold mb-4">P&L Data</h1>
            <form onSubmit={handleSubmit} className="mb-6">
                <div className="mb-4">
                    <label htmlFor="storeId" className="block text-sm font-medium text-gray-700">Store ID:</label>
                    <input
                        type="text"
                        id="storeId"
                        value={storeId}
                        onChange={handleStoreIdChange}
                        required
                        className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                    />
                </div>
                <div className="mb-4">
                    <label htmlFor="startDate" className="block text-sm font-medium text-gray-700">Start Date:</label>
                    <input
                        type="date"
                        id="startDate"
                        value={startDate}
                        onChange={handleStartDateChange}
                        required
                        className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                    />
                </div>
                <div className="mb-4">
                    <label htmlFor="endDate" className="block text-sm font-medium text-gray-700">End Date:</label>
                    <input
                        type="date"
                        id="endDate"
                        value={endDate}
                        onChange={handleEndDateChange}
                        required
                        className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                    />
                </div>
                <button type="submit" className="px-4 py-2 bg-blue-500 text-white rounded-md shadow-sm hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                    Get P&L Data
                </button>
            </form>
            {error && <p className="text-red-500">{error}</p>}
            {pnlData && (
                <div className="overflow-x-auto">
                    <table className="min-w-full divide-y divide-gray-200">
                        <thead className="bg-gray-50">
                            <tr>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Order Date</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Selling Price</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Cost Price</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Logistic Charges</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Profit</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Order Count</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Cancelled Count</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Delivered Count</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">RTO Count</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Cancelled %</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Delivered %</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">RTO %</th>
                            </tr>
                        </thead>
                        <tbody className="bg-white divide-y divide-gray-200">
                            {pnlData.map((item, index) => (
                                <tr key={index}>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{item.order_date}</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{item.selling_price}</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{item.cost_price}</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{item.logistic_charges}</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{item.profit}</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{item.order_count}</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{item.cancelled_count}</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{item.delivered_count}</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{item.rto_count}</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{item.cancelled_percentage.toFixed(2)}%</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{item.delivered_percentage.toFixed(2)}%</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{item.rto_percentage.toFixed(2)}%</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}
        </div>
    );
};

export default PnlForm;
