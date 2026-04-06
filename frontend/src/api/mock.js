// Mock API for Expense Auditor

const mockExpenses = [
  {
    id: 1,
    date: '2023-11-20',
    merchant: 'Delta Airlines',
    amount: 450.00,
    purpose: 'Client meeting in NYC',
    verdict: 'Approved',
    citation: 'Section 3.1: Air travel approved for client meetings.',
  },
  {
    id: 2,
    date: '2023-11-22',
    merchant: 'Ritz Carlton',
    amount: 1200.00,
    purpose: 'Hotel stay during conference',
    verdict: 'Flagged',
    citation: 'Section 4.2: Hotel costs exceed standard $300/night limit.',
  },
  {
    id: 3,
    date: '2023-11-23',
    merchant: 'Steakhouse',
    amount: 150.00,
    purpose: 'Dinner with client',
    verdict: 'Approved',
    citation: 'Section 5.1: Per diem for meals is $75/person. 2 persons.',
  },
  {
    id: 4,
    date: '2023-11-25',
    merchant: 'Apple Store',
    amount: 2500.00,
    purpose: 'New Macbook for personal use',
    verdict: 'Rejected',
    citation: 'Section 1.4: Personal electronics are strictly prohibited.',
  }
];

export const uploadReceipt = async (formData) => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        status: 'success',
        message: 'Receipt uploaded successfully. Analysis in progress.',
      });
    }, 1500);
  });
};

export const fetchExpenses = async () => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve(mockExpenses);
    }, 800);
  });
};
