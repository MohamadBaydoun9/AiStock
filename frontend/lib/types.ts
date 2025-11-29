export interface Product {
  _id?: string
  productType: string
  productName: string
  predictedPrice: number
  price: number
  quantity: number
  imageUrl: string
  dateAdded: string
}

export interface ClassificationResult {
  productType: string;
  productName: string;
  predictedPrice: number;
  imageUrl: string;
  confidence: number;
  predictedBreed?: string;
  predictionConfidence?: number;
  metadata?: {
    age_months?: number;
    weight_kg?: number;
    health_status?: number;
    vaccinated?: boolean;
    country?: string;
  };
}
