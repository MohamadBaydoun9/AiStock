"use client"

import { useState, useEffect } from "react"
import { useRouter } from 'next/navigation'
import { ArrowLeft, BarChart3, CheckCircle2, XCircle, AlertTriangle, Brain, TrendingUp } from 'lucide-react'
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table"
import { Progress } from "@/components/ui/progress"
import { api, Product } from "@/lib/api"
import AuthGuard from "@/components/auth-guard"

export default function ModelStatsPage() {
    const router = useRouter()
    const [products, setProducts] = useState<Product[]>([])
    const [isLoading, setIsLoading] = useState(true)

    useEffect(() => {
        loadData()
    }, [])

    const loadData = async () => {
        try {
            // Fetch all products (limit 1000 for stats)
            const allProducts = await api.getProducts({ limit: 1000 } as any)
            setProducts(allProducts)
        } catch (error) {
            console.error("Failed to load products:", error)
        } finally {
            setIsLoading(false)
        }
    }

    // Calculate Statistics
    const totalProducts = products.length
    const productsWithPrediction = products.filter(p => p.predicted_breed)
    const totalPredictions = productsWithPrediction.length

    // Accuracy: Where predicted breed matches actual product name (assuming product name is breed)
    const correctPredictions = productsWithPrediction.filter(
        p => p.predicted_breed?.toLowerCase() === p.product_name.toLowerCase()
    )
    const accuracy = totalPredictions > 0 ? (correctPredictions.length / totalPredictions) * 100 : 0

    // User Overrides: Where predicted breed != actual product name
    const overrides = totalPredictions - correctPredictions.length
    const overrideRate = totalPredictions > 0 ? (overrides / totalPredictions) * 100 : 0

    // Average Confidence
    const avgConfidence = totalPredictions > 0
        ? productsWithPrediction.reduce((acc, p) => acc + (p.prediction_confidence || 0), 0) / totalPredictions
        : 0

    // Price Accuracy (MAE)
    const pricePredictions = products.filter(p => p.price_predicted > 0)
    const mae = pricePredictions.length > 0
        ? pricePredictions.reduce((acc, p) => acc + Math.abs(p.price_predicted - (p.price_modified || p.price_predicted)), 0) / pricePredictions.length
        : 0

    return (
        <AuthGuard>
            <div className="min-h-screen bg-background">
                <div className="container mx-auto px-4 py-8 max-w-7xl">
                    {/* Header */}
                    <div className="flex items-center justify-between mb-8">
                        <div className="flex items-center gap-4">
                            <Button variant="ghost" size="icon" onClick={() => router.back()}>
                                <ArrowLeft className="h-6 w-6" />
                            </Button>
                            <div>
                                <h1 className="text-3xl font-bold tracking-tight">Model Performance</h1>
                                <p className="text-muted-foreground">
                                    Real-time statistics on AI classification and pricing accuracy
                                </p>
                            </div>
                        </div>
                        <Button onClick={loadData} variant="outline">
                            Refresh Data
                        </Button>
                    </div>

                    {/* Key Metrics */}
                    <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4 mb-8">
                        <Card>
                            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                                <CardTitle className="text-sm font-medium">Classification Accuracy</CardTitle>
                                <CheckCircle2 className="h-4 w-4 text-green-500" />
                            </CardHeader>
                            <CardContent>
                                <div className="text-2xl font-bold">{accuracy.toFixed(1)}%</div>
                                <p className="text-xs text-muted-foreground">
                                    {correctPredictions.length} correct out of {totalPredictions}
                                </p>
                                <Progress value={accuracy} className="mt-3" />
                            </CardContent>
                        </Card>

                        <Card>
                            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                                <CardTitle className="text-sm font-medium">Avg. Confidence</CardTitle>
                                <Brain className="h-4 w-4 text-blue-500" />
                            </CardHeader>
                            <CardContent>
                                <div className="text-2xl font-bold">{(avgConfidence * 100).toFixed(1)}%</div>
                                <p className="text-xs text-muted-foreground">
                                    Model certainty on predictions
                                </p>
                                <Progress value={avgConfidence * 100} className="mt-3" />
                            </CardContent>
                        </Card>

                        <Card>
                            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                                <CardTitle className="text-sm font-medium">User Override Rate</CardTitle>
                                <AlertTriangle className="h-4 w-4 text-yellow-500" />
                            </CardHeader>
                            <CardContent>
                                <div className="text-2xl font-bold">{overrideRate.toFixed(1)}%</div>
                                <p className="text-xs text-muted-foreground">
                                    {overrides} predictions changed by user
                                </p>
                                <Progress value={overrideRate} className="mt-3 bg-yellow-100" />
                            </CardContent>
                        </Card>

                        <Card>
                            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                                <CardTitle className="text-sm font-medium">Price Error (MAE)</CardTitle>
                                <TrendingUp className="h-4 w-4 text-purple-500" />
                            </CardHeader>
                            <CardContent>
                                <div className="text-2xl font-bold">${mae.toFixed(2)}</div>
                                <p className="text-xs text-muted-foreground">
                                    Avg. difference: Predicted vs Actual
                                </p>
                            </CardContent>
                        </Card>
                    </div>

                    {/* Detailed Table */}
                    <Card>
                        <CardHeader>
                            <CardTitle>Prediction History</CardTitle>
                            <CardDescription>
                                Recent products and their AI prediction details
                            </CardDescription>
                        </CardHeader>
                        <CardContent>
                            <Table>
                                <TableHeader>
                                    <TableRow>
                                        <TableHead>Product Name (Actual)</TableHead>
                                        <TableHead>Predicted Breed</TableHead>
                                        <TableHead>Confidence</TableHead>
                                        <TableHead>Predicted Price</TableHead>
                                        <TableHead>Actual Price</TableHead>
                                        <TableHead>Status</TableHead>
                                    </TableRow>
                                </TableHeader>
                                <TableBody>
                                    {productsWithPrediction.length === 0 ? (
                                        <TableRow>
                                            <TableCell colSpan={6} className="text-center py-8 text-muted-foreground">
                                                No prediction data available yet. Add products to see stats.
                                            </TableCell>
                                        </TableRow>
                                    ) : (
                                        productsWithPrediction.slice(0, 20).map((product) => {
                                            const isMatch = product.predicted_breed?.toLowerCase() === product.product_name.toLowerCase()
                                            const confidence = (product.prediction_confidence || 0) * 100

                                            return (
                                                <TableRow key={product._id}>
                                                    <TableCell className="font-medium">{product.product_name}</TableCell>
                                                    <TableCell>
                                                        <div className="flex items-center gap-2">
                                                            {product.predicted_breed || "N/A"}
                                                        </div>
                                                    </TableCell>
                                                    <TableCell>
                                                        <div className="flex items-center gap-2">
                                                            <div className={`h-2 w-16 rounded-full bg-secondary overflow-hidden`}>
                                                                <div
                                                                    className={`h-full ${confidence > 80 ? 'bg-green-500' : confidence > 50 ? 'bg-yellow-500' : 'bg-red-500'}`}
                                                                    style={{ width: `${confidence}%` }}
                                                                />
                                                            </div>
                                                            <span className="text-xs text-muted-foreground">{confidence.toFixed(0)}%</span>
                                                        </div>
                                                    </TableCell>
                                                    <TableCell>${product.price_predicted.toFixed(2)}</TableCell>
                                                    <TableCell>${(product.price_modified || product.price_predicted).toFixed(2)}</TableCell>
                                                    <TableCell>
                                                        {isMatch ? (
                                                            <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                                                                Match
                                                            </span>
                                                        ) : (
                                                            <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
                                                                Override
                                                            </span>
                                                        )}
                                                    </TableCell>
                                                </TableRow>
                                            )
                                        })
                                    )}
                                </TableBody>
                            </Table>
                        </CardContent>
                    </Card>
                </div>
            </div>
        </AuthGuard>
    )
}
