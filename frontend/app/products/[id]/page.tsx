"use client"

import { useState, useEffect, use } from "react"
import { useRouter } from 'next/navigation'
import Image from "next/image"
import { ArrowLeft, Edit, Trash2, Package, DollarSign, Hash, Calendar, TrendingUp } from 'lucide-react'
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog"
import { useToast } from "@/hooks/use-toast"
import { api, Product } from "@/lib/api"
import AuthGuard from "@/components/auth-guard"

export default function ProductDetailsPage({
  params,
}: {
  params: Promise<{ id: string }>
}) {
  const { id } = use(params)
  const router = useRouter()
  const { toast } = useToast()
  const [product, setProduct] = useState<Product | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false)

  useEffect(() => {
    fetchProduct()
  }, [id])

  const fetchProduct = async () => {
    try {
      const data = await api.getProduct(id)
      setProduct(data)
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to load product details",
        variant: "destructive"
      })
      console.error('Fetch error:', error)
      router.push('/dashboard')
    } finally {
      setIsLoading(false)
    }
  }

  const handleDelete = async () => {
    try {
      const token = localStorage.getItem('token')
      const response = await fetch(`http://localhost:8000/products/${id}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })

      if (!response.ok) throw new Error('Failed to delete product')

      toast({
        title: "Product Deleted",
        description: "The product has been removed from inventory",
      })
      router.push('/dashboard')
    } catch (error) {
      toast({
        title: "Delete Failed",
        description: "Unable to delete product",
        variant: "destructive"
      })
      console.error('Delete error:', error)
    }
  }

  if (isLoading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="text-center py-12 text-muted-foreground">
          Loading product details...
        </div>
      </div>
    )
  }

  if (!product) {
    return null
  }

  const currentPrice = product.price_modified ?? product.price_predicted
  const totalValue = currentPrice * product.quantity
  const priceDifference = currentPrice - product.price_predicted
  const priceChangePercent = ((priceDifference / product.price_predicted) * 100).toFixed(1)

  return (
    <AuthGuard>
      <div className="container mx-auto px-4 py-8 max-w-5xl">
        <Button
          variant="ghost"
          onClick={() => router.push('/dashboard')}
          className="mb-6"
        >
          <ArrowLeft className="mr-2 h-4 w-4" />
          Back to Dashboard
        </Button>

        <div className="grid gap-6 lg:grid-cols-2 mb-6">
          {/* Product Image */}
          <Card className="border-2">
            <CardHeader>
              <CardTitle>Product Image</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="relative w-full aspect-square rounded-lg overflow-hidden border-2 border-border bg-muted">
                {product.has_image ? (
                  <img
                    src={`http://localhost:8000/products/${product.product_id}/image`}
                    alt={product.product_name}
                    className="object-cover w-full h-full"
                  />
                ) : (
                  <div className="flex items-center justify-center h-full bg-muted text-muted-foreground">
                    <Package className="h-16 w-16" />
                  </div>
                )}
              </div>
            </CardContent>
          </Card>

          {/* Product Information */}
          <Card className="border-2">
            <CardHeader>
              <CardTitle className="text-2xl">{product.product_name}</CardTitle>
              <CardDescription>
                <span className="inline-flex items-center rounded-full bg-primary/10 px-3 py-1 text-sm font-medium text-primary">
                  {product.product_type}
                </span>
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-3">
                <div className="flex items-center justify-between p-4 rounded-lg bg-muted">
                  <div className="flex items-center gap-2 text-muted-foreground">
                    <DollarSign className="h-5 w-5" />
                    <span className="font-medium">Current Price</span>
                  </div>
                  <span className="text-2xl font-bold">${currentPrice.toFixed(2)}</span>
                </div>

                <div className="flex items-center justify-between p-4 rounded-lg bg-muted">
                  <div className="flex items-center gap-2 text-muted-foreground">
                    <Hash className="h-5 w-5" />
                    <span className="font-medium">Quantity in Stock</span>
                  </div>
                  <span className="text-2xl font-bold">{product.quantity}</span>
                </div>

                <div className="flex items-center justify-between p-4 rounded-lg bg-primary/10 border border-primary/20">
                  <div className="flex items-center gap-2 text-muted-foreground">
                    <Package className="h-5 w-5" />
                    <span className="font-medium">Total Value</span>
                  </div>
                  <span className="text-2xl font-bold text-primary">
                    ${totalValue.toFixed(2)}
                  </span>
                </div>
              </div>

              <div className="pt-4 space-y-2">
                <Button
                  onClick={() => router.push(`/products/${id}/edit`)}
                  size="lg"
                  className="w-full"
                >
                  <Edit className="mr-2 h-4 w-4" />
                  Edit Product
                </Button>

                <Button
                  onClick={() => setDeleteDialogOpen(true)}
                  variant="destructive"
                  size="lg"
                  className="w-full"
                >
                  <Trash2 className="mr-2 h-4 w-4" />
                  Delete Product
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Additional Details */}
        <div className="grid gap-6 md:grid-cols-2">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <TrendingUp className="h-5 w-5 text-primary" />
                AI Prediction
              </CardTitle>
              <CardDescription>
                Machine learning price prediction
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-sm text-muted-foreground">Predicted Price</span>
                <span className="font-semibold">${product.price_predicted.toFixed(2)}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-muted-foreground">Your Price</span>
                <span className="font-semibold">${currentPrice.toFixed(2)}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-muted-foreground">Difference</span>
                <span className={`font-semibold ${priceDifference >= 0 ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'}`}>
                  {priceDifference >= 0 ? '+' : ''}{priceDifference.toFixed(2)} ({priceChangePercent}%)
                </span>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Calendar className="h-5 w-5 text-primary" />
                Product History
              </CardTitle>
              <CardDescription>
                Inventory tracking information
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-sm text-muted-foreground">Date Added</span>
                <span className="font-semibold">
                  {new Date(product.date_added).toLocaleDateString('en-US', {
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric'
                  })}
                </span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-muted-foreground">Time Added</span>
                <span className="font-semibold">
                  {new Date(product.date_added).toLocaleTimeString('en-US', {
                    hour: '2-digit',
                    minute: '2-digit'
                  })}
                </span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-muted-foreground">Product ID</span>
                <span className="font-mono text-xs">{product.product_id}</span>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Metadata Card */}
        {(product.age_months !== undefined || product.weight_kg !== undefined || product.health_status !== undefined || product.vaccinated !== undefined) && (
          <Card className="mb-6">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Package className="h-5 w-5 text-primary" />
                Pet Metadata
              </CardTitle>
              <CardDescription>
                Additional information about the pet
              </CardDescription>
            </CardHeader>
            <CardContent className="grid gap-3 md:grid-cols-2">
              {product.age_months !== undefined && (
                <div className="flex justify-between items-center p-3 rounded-lg bg-muted">
                  <span className="text-sm text-muted-foreground">Age</span>
                  <span className="font-semibold">{product.age_months} months</span>
                </div>
              )}
              {product.weight_kg !== undefined && (
                <div className="flex justify-between items-center p-3 rounded-lg bg-muted">
                  <span className="text-sm text-muted-foreground">Weight</span>
                  <span className="font-semibold">{product.weight_kg} kg</span>
                </div>
              )}
              {product.health_status !== undefined && (
                <div className="flex justify-between items-center p-3 rounded-lg bg-muted">
                  <span className="text-sm text-muted-foreground">Health Status</span>
                  <span className="font-semibold">
                    {["Normal", "Good", "Excellent"][product.health_status]}
                  </span>
                </div>
              )}
              {product.vaccinated !== undefined && (
                <div className="flex justify-between items-center p-3 rounded-lg bg-muted">
                  <span className="text-sm text-muted-foreground">Vaccinated</span>
                  <span className="font-semibold">{product.vaccinated ? "Yes" : "No"}</span>
                </div>
              )}
              {product.country && (
                <div className="flex justify-between items-center p-3 rounded-lg bg-muted">
                  <span className="text-sm text-muted-foreground">Country of Origin</span>
                  <span className="font-semibold">{product.country}</span>
                </div>
              )}
            </CardContent>
          </Card>
        )}

        {/* Delete Confirmation Dialog */}
        <AlertDialog open={deleteDialogOpen} onOpenChange={setDeleteDialogOpen}>
          <AlertDialogContent>
            <AlertDialogHeader>
              <AlertDialogTitle>Delete {product.product_name}?</AlertDialogTitle>
              <AlertDialogDescription>
                This action cannot be undone. This will permanently delete the product from your inventory.
              </AlertDialogDescription>
            </AlertDialogHeader>
            <AlertDialogFooter>
              <AlertDialogCancel>Cancel</AlertDialogCancel>
              <AlertDialogAction
                onClick={handleDelete}
                className="bg-destructive text-destructive-foreground hover:bg-destructive/90"
              >
                Delete Product
              </AlertDialogAction>
            </AlertDialogFooter>
          </AlertDialogContent>
        </AlertDialog>
      </div>
    </AuthGuard>
  )
}
