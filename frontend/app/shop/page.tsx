"use client"

import { useState, useEffect } from "react"
import Image from "next/image"
import { useRouter } from "next/navigation"
import { Search, Filter, X, Heart, Calendar, Weight, Syringe, Eye } from 'lucide-react'
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardFooter, CardHeader } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select"
import { Slider } from "@/components/ui/slider"
import { Product } from "@/lib/api"

export default function ShopPage() {
    const router = useRouter()
    const [products, setProducts] = useState<Product[]>([])
    const [isLoading, setIsLoading] = useState(true)

    // Filters
    const [selectedType, setSelectedType] = useState<string>("all")
    const [selectedBreed, setSelectedBreed] = useState<string>("")
    const [priceRange, setPriceRange] = useState<number[]>([0, 5000])
    const [showFilters, setShowFilters] = useState(false)

    // Available types and breeds
    const [productTypes, setProductTypes] = useState<string[]>([])
    const [breeds, setBreeds] = useState<string[]>([])

    useEffect(() => {
        fetchProducts()
        fetchTypes()
    }, [selectedType, selectedBreed, priceRange])

    const fetchProducts = async () => {
        setIsLoading(true)
        try {
            const params = new URLSearchParams()
            if (selectedType && selectedType !== 'all') params.append('type', selectedType)
            if (selectedBreed) params.append('breed', selectedBreed)
            params.append('min_price', priceRange[0].toString())
            params.append('max_price', priceRange[1].toString())

            const response = await fetch(`http://localhost:8000/products/shop/published?${params}`)
            if (response.ok) {
                const data = await response.json()
                setProducts(data)
            }
        } catch (error) {
            console.error('Failed to fetch products:', error)
        } finally {
            setIsLoading(false)
        }
    }

    const fetchTypes = async () => {
        try {
            const response = await fetch('http://localhost:8000/product-types')
            if (response.ok) {
                const data = await response.json()
                setProductTypes(data.map((t: any) => t.name))
            }
        } catch (error) {
            console.error('Failed to fetch types:', error)
        }
    }

    const clearFilters = () => {
        setSelectedType("all")
        setSelectedBreed("")
        setPriceRange([0, 5000])
    }

    const healthLabels = ['Normal', 'Good', 'Excellent']

    return (
        <div className="min-h-screen bg-gradient-to-br from-background via-background to-primary/5">
            {/* Header */}
            <div className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
                <div className="container mx-auto px-4 py-6">
                    <div className="flex items-center justify-between">
                        <div>
                            <h1 className="text-4xl font-bold bg-gradient-to-r from-primary to-primary/60 bg-clip-text text-transparent">
                                Pet Shop
                            </h1>
                            <p className="text-muted-foreground mt-1">
                                Find your perfect companion
                            </p>
                        </div>
                        <div className="flex gap-2">
                            <Button
                                onClick={() => router.push('/dashboard')}
                                variant="default"
                                className="hidden md:flex"
                            >
                                Dashboard
                            </Button>
                            <Button
                                variant="outline"
                                onClick={() => setShowFilters(!showFilters)}
                                className="lg:hidden"
                            >
                                <Filter className="h-4 w-4 mr-2" />
                                Filters
                            </Button>
                        </div>
                    </div>
                </div>
            </div>

            <div className="container mx-auto px-4 py-8">
                <div className="flex gap-6">
                    {/* Filters Sidebar */}
                    <aside className={`${showFilters ? 'block' : 'hidden'} lg:block w-full lg:w-64 flex-shrink-0`}>
                        <Card className="sticky top-4 border-2">
                            <CardHeader>
                                <div className="flex items-center justify-between">
                                    <h2 className="text-lg font-semibold flex items-center gap-2">
                                        <Filter className="h-5 w-5 text-primary" />
                                        Filters
                                    </h2>
                                    <Button
                                        variant="ghost"
                                        size="sm"
                                        onClick={clearFilters}
                                    >
                                        <X className="h-4 w-4" />
                                    </Button>
                                </div>
                            </CardHeader>
                            <CardContent className="space-y-6">
                                {/* Pet Type */}
                                <div className="space-y-2">
                                    <Label>Pet Type</Label>
                                    <Select value={selectedType} onValueChange={setSelectedType}>
                                        <SelectTrigger>
                                            <SelectValue placeholder="All Types" />
                                        </SelectTrigger>
                                        <SelectContent>
                                            <SelectItem value="all">All Types</SelectItem>
                                            {productTypes.map((type) => (
                                                <SelectItem key={type} value={type}>
                                                    {type}
                                                </SelectItem>
                                            ))}
                                        </SelectContent>
                                    </Select>
                                </div>

                                {/* Breed Search */}
                                <div className="space-y-2">
                                    <Label>Breed</Label>
                                    <Input
                                        placeholder="Search breed..."
                                        value={selectedBreed}
                                        onChange={(e) => setSelectedBreed(e.target.value)}
                                    />
                                </div>

                                {/* Price Range */}
                                <div className="space-y-3">
                                    <Label>Price Range</Label>
                                    <div className="px-2">
                                        <Slider
                                            min={0}
                                            max={5000}
                                            step={50}
                                            value={priceRange}
                                            onValueChange={setPriceRange}
                                            className="w-full"
                                        />
                                    </div>
                                    <div className="flex justify-between text-sm text-muted-foreground">
                                        <span>${priceRange[0]}</span>
                                        <span>${priceRange[1]}</span>
                                    </div>
                                </div>

                                <Button
                                    onClick={clearFilters}
                                    variant="outline"
                                    className="w-full"
                                >
                                    Clear All Filters
                                </Button>
                            </CardContent>
                        </Card>
                    </aside>

                    {/* Products Grid */}
                    <main className="flex-1">
                        {isLoading ? (
                            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                                {[1, 2, 3, 4, 5, 6].map((i) => (
                                    <Card key={i} className="animate-pulse">
                                        <div className="aspect-square bg-muted rounded-t-lg" />
                                        <CardContent className="p-4 space-y-2">
                                            <div className="h-4 bg-muted rounded w-3/4" />
                                            <div className="h-4 bg-muted rounded w-1/2" />
                                        </CardContent>
                                    </Card>
                                ))}
                            </div>
                        ) : products.length === 0 ? (
                            <Card className="border-2 border-dashed">
                                <CardContent className="flex flex-col items-center justify-center py-16">
                                    <div className="h-16 w-16 rounded-full bg-muted flex items-center justify-center mb-4">
                                        <Search className="h-8 w-8 text-muted-foreground" />
                                    </div>
                                    <h3 className="text-xl font-semibold mb-2">No pets found</h3>
                                    <p className="text-muted-foreground text-center max-w-md">
                                        Try adjusting your filters or check back later for new additions
                                    </p>
                                    <Button onClick={clearFilters} className="mt-4">
                                        Clear Filters
                                    </Button>
                                </CardContent>
                            </Card>
                        ) : (
                            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                                {products.map((product) => {
                                    const price = product.price_modified ?? product.price_predicted
                                    return (
                                        <Card
                                            key={product.product_id}
                                            className="group overflow-hidden border-2 hover:border-primary/50 transition-all duration-300 hover:shadow-xl hover:scale-[1.02] cursor-pointer"
                                            onClick={() => router.push(`/shop/${product.product_id}`)}
                                        >
                                            {/* Image */}
                                            <div className="relative aspect-square overflow-hidden bg-gradient-to-br from-primary/5 to-primary/10">
                                                {product.has_image ? (
                                                    <img
                                                        src={`http://localhost:8000/products/${product.product_id}/image`}
                                                        alt={product.product_name}
                                                        className="object-cover w-full h-full group-hover:scale-110 transition-transform duration-300"
                                                    />
                                                ) : (
                                                    <div className="flex items-center justify-center h-full">
                                                        <Heart className="h-16 w-16 text-muted-foreground" />
                                                    </div>
                                                )}
                                                {/* Type Badge */}
                                                <div className="absolute top-3 left-3">
                                                    <span className="inline-flex items-center rounded-full bg-primary/90 backdrop-blur px-3 py-1 text-sm font-medium text-primary-foreground">
                                                        {product.product_type}
                                                    </span>
                                                </div>
                                            </div>

                                            {/* Content */}
                                            <CardContent className="p-4 space-y-3">
                                                <div>
                                                    <h3 className="font-bold text-lg line-clamp-1">
                                                        {product.product_name}
                                                    </h3>
                                                    <p className="text-sm text-muted-foreground">
                                                        {product.product_type}
                                                    </p>
                                                </div>

                                                {/* Metadata Badges */}
                                                <div className="flex flex-wrap gap-2">
                                                    {product.age_months != null && (
                                                        <span className="inline-flex items-center gap-1 rounded-full bg-muted px-2.5 py-0.5 text-xs font-medium">
                                                            <Calendar className="h-3 w-3" />
                                                            {product.age_months}mo
                                                        </span>
                                                    )}
                                                    {product.weight_kg != null && (
                                                        <span className="inline-flex items-center gap-1 rounded-full bg-muted px-2.5 py-0.5 text-xs font-medium">
                                                            <Weight className="h-3 w-3" />
                                                            {product.weight_kg}kg
                                                        </span>
                                                    )}
                                                    {product.health_status != null && (
                                                        <span className="inline-flex items-center gap-1 rounded-full bg-muted px-2.5 py-0.5 text-xs font-medium">
                                                            <Heart className="h-3 w-3" />
                                                            {healthLabels[product.health_status]}
                                                        </span>
                                                    )}
                                                    {product.vaccinated && (
                                                        <span className="inline-flex items-center gap-1 rounded-full bg-green-100 dark:bg-green-900/30 px-2.5 py-0.5 text-xs font-medium text-green-700 dark:text-green-400">
                                                            <Syringe className="h-3 w-3" />
                                                            Vaccinated
                                                        </span>
                                                    )}
                                                    {product.country && (
                                                        <span className="inline-flex items-center gap-1 rounded-full bg-blue-100 dark:bg-blue-900/30 px-2.5 py-0.5 text-xs font-medium text-blue-700 dark:text-blue-400">
                                                            🌍 {product.country}
                                                        </span>
                                                    )}
                                                </div>
                                            </CardContent>

                                            {/* Footer with Price */}
                                            <CardFooter className="p-4 pt-0">
                                                <div className="w-full">
                                                    <p className="text-2xl font-bold text-primary">
                                                        ${price.toFixed(2)}
                                                    </p>
                                                    {product.quantity > 0 ? (
                                                        <p className="text-xs text-muted-foreground">
                                                            {product.quantity} available
                                                        </p>
                                                    ) : (
                                                        <p className="text-xs text-destructive">
                                                            Out of stock
                                                        </p>
                                                    )}
                                                </div>
                                            </CardFooter>
                                        </Card>
                                    )
                                })}
                            </div>
                        )}

                        {/* Results Count */}
                        {!isLoading && products.length > 0 && (
                            <div className="mt-8 text-center text-sm text-muted-foreground">
                                Showing {products.length} {products.length === 1 ? 'pet' : 'pets'}
                            </div>
                        )}
                    </main>
                </div>
            </div>
        </div >
    )
}
