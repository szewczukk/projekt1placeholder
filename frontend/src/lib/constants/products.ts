export type Product = {
	id: number;
	name: string;
	price: number;
	description: string;
};

export const products: Product[] = [
	{
		id: 1,
		name: "Product 1",
		price: 100,
		description: "Prosty opis produktu 1.",
	},
	{
		id: 2,
		name: "Product 2",
		price: 150,
		description: "Prosty opis produktu 2.",
	},
	{
		id: 3,
		name: "Product 3",
		price: 400,
		description: "Prosty opis produktu 3.",
	},
];
