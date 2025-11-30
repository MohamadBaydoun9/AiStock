"use client"

import { useState, useEffect } from "react"
import { useRouter } from 'next/navigation'
import Image from "next/image"
import { Upload, Loader2, CheckCircle2, XCircle, Camera, Edit, DollarSign, Info } from 'lucide-react'
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { useToast } from "@/hooks/use-toast"
import type { ClassificationResult } from "@/lib/types"
import { api, ProductType } from "@/lib/api"
import AuthGuard from "@/components/auth-guard"

export default function UploadPage() {
  const router = useRouter()
  const { toast } = useToast()
  const [selectedImage, setSelectedImage] = useState<File | null>(null)
  const [previewUrl, setPreviewUrl] = useState<string>("")
  const [isClassifying, setIsClassifying] = useState(false)
  const [classificationResult, setClassificationResult] = useState<ClassificationResult | null>(null)

  // Step management
  const [currentStep, setCurrentStep] = useState<'upload' | 'classify' | 'metadata' | 'review'>("upload")

  // Editable classification fields
  const [productTypes, setProductTypes] = useState<ProductType[]>([])
  const [editedType, setEditedType] = useState<string>("")
  const [editedName, setEditedName] = useState<string>("")
  const [isLoadingTypes, setIsLoadingTypes] = useState(false)

  // Metadata fields
  const [ageMonths, setAgeMonths] = useState<string>("")
  const [weightKg, setWeightKg] = useState<string>("")
  const [healthStatus, setHealthStatus] = useState<string>("1")
  const [vaccinated, setVaccinated] = useState<boolean>(false)
  const [country, setCountry] = useState<string>("USA")

  // Price prediction
  const [isPredictingPrice, setIsPredictingPrice] = useState(false)
  const [predictedPrice, setPredictedPrice] = useState<number | null>(null)

  useEffect(() => {
    fetchProductTypes()
  }, [])

  const fetchProductTypes = async () => {
    setIsLoadingTypes(true)
    try {
      const types = await api.getProductTypes()
      setProductTypes(types)
    } catch (error) {
      console.error('Failed to fetch product types:', error)
    } finally {
      setIsLoadingTypes(false)
    }
  }

  const handleImageSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      if (!file.type.startsWith('image/')) {
        toast({
          title: "Invalid file type",
          description: "Please select an image file",
          variant: "destructive"
        })
        return
      }

      setSelectedImage(file)
      const url = URL.createObjectURL(file)
      setPreviewUrl(url)
      setClassificationResult(null)
      setEditedType("")
      setEditedName("")
      setCurrentStep("upload")
      setPredictedPrice(null)
    }
  }

  const handleUploadAndClassify = async () => {
    if (!selectedImage) return

    setIsClassifying(true)

    try {
      const formData = new FormData()
      formData.append('file', selectedImage)

      const result = await api.classifyImage(formData)

      console.log('Backend response:', result)

      // Debug: Log prediction details
      console.log('=== PREDICTION DEBUG ===')
      console.log('Product Type:', result.product_type)
      console.log('Predicted Breed:', result.product_name)
      console.log('Confidence:', `${(result.confidence * 100).toFixed(2)}%`)
      console.log('========================')

      setClassificationResult({
        productName: result.product_name,
        productType: result.product_type,
        predictedPrice: result.price_predicted,
        imageUrl: previewUrl,
        confidence: result.confidence
      })

      // Pre-fill editable fields with AI predictions
      setEditedType(result.product_type)
      setEditedName(result.product_name)
      setCurrentStep("classify")

      toast({
        title: "Classification Complete",
        description: `Detected: ${result.product_name}`,
      })
    } catch (error) {
      console.error('Classification error:', error)
      toast({
        title: "Classification Failed",
        description: "Unable to classify the product. Please try again.",
        variant: "destructive"
      })
    } finally {
      setIsClassifying(false)
    }
  }

  const handleConfirmClassification = () => {
    if (!editedType || !editedName) {
      toast({
        title: "Missing Information",
        description: "Please confirm product type and name",
        variant: "destructive"
      })
      return
    }

    setCurrentStep("metadata")
  }

  const handlePredictPrice = async () => {
    if (!selectedImage || !editedType || !editedName) {
      toast({
        title: "Missing Information",
        description: "Please complete all fields",
        variant: "destructive"
      })
      return
    }

    // Validate metadata
    const age = parseInt(ageMonths)
    const weight = parseFloat(weightKg)

    if (isNaN(age) || age < 1 || age > 120) {
      toast({
        title: "Invalid Age",
        description: "Please enter a valid age between 1-120 months",
        variant: "destructive"
      })
      return
    }

    if (isNaN(weight) || weight <= 0 || weight > 200) {
      toast({
        title: "Invalid Weight",
        description: "Please enter a valid weight between 0-200 kg",
        variant: "destructive"
      })
      return
    }

    setIsPredictingPrice(true)

    try {
      const formData = new FormData()
      formData.append('image', selectedImage)
      formData.append('pet_type', editedType)
      formData.append('breed', editedName)
      formData.append('age_months', ageMonths)
      formData.append('weight_kg', weightKg)
      formData.append('health_status', healthStatus)
      formData.append('vaccinated', vaccinated.toString())
      formData.append('country', country)

      const response = await fetch('http://localhost:8000/ml/predict-price', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: formData
      })

      if (!response.ok) {
        throw new Error('Price prediction failed')
      }

      const result = await response.json()
      setPredictedPrice(result.predicted_price)
      setCurrentStep("review")

      toast({
        title: "Price Predicted",
        description: `Estimated price: $${result.predicted_price.toFixed(2)}`,
      })
    } catch (error) {
      console.error('Price prediction error:', error)
      toast({
        title: "Price Prediction Failed",
        description: "Using default price estimation",
        variant: "destructive"
      })
      // Fallback to classification price
      setPredictedPrice(classificationResult?.predictedPrice || 0)
      setCurrentStep("review")
    } finally {
      setIsPredictingPrice(false)
    }
  }

  const handleContinue = () => {
    if (!classificationResult || predictedPrice === null) return

    // Store the edited result in sessionStorage
    sessionStorage.setItem('classificationResult', JSON.stringify({
      productType: editedType,
      productName: editedName,
      predictedPrice: predictedPrice,
      imageUrl: previewUrl,
      predictedBreed: classificationResult.productName,
      predictionConfidence: classificationResult.confidence,
      metadata: {
        age_months: parseInt(ageMonths),
        weight_kg: parseFloat(weightKg),
        health_status: parseInt(healthStatus),
        vaccinated: vaccinated,
        country: country
      }
    }))
    router.push('/add-product')
  }

  const handleRetry = () => {
    setSelectedImage(null)
    setPreviewUrl("")
    setClassificationResult(null)
    setEditedType("")
    setEditedName("")
    setCurrentStep("upload")
    setAgeMonths("")
    setWeightKg("")
    setHealthStatus("1")
    setVaccinated(true)
    setPredictedPrice(null)
  }

  const handleBack = () => {
    if (currentStep === "metadata") {
      setCurrentStep("classify")
    } else if (currentStep === "review") {
      setCurrentStep("metadata")
    }
  }

  return (
    <AuthGuard>
      <div className="container mx-auto px-4 py-8 max-w-4xl">
        <div className="mb-8 text-center">
          <h1 className="text-4xl font-bold mb-3 text-balance">Upload Product Image</h1>
          <p className="text-muted-foreground text-lg text-pretty">
            Use AI to automatically classify your product and predict its price
          </p>
        </div>

        {/* Progress Indicator */}
        <div className="mb-6 flex justify-center">
          <div className="flex items-center gap-2">
            <div className={`h-2 w-20 rounded-full ${currentStep !== 'upload' ? 'bg-primary' : 'bg-muted'}`} />
            <div className={`h-2 w-20 rounded-full ${currentStep === 'metadata' || currentStep === 'review' ? 'bg-primary' : 'bg-muted'}`} />
            <div className={`h-2 w-20 rounded-full ${currentStep === 'review' ? 'bg-primary' : 'bg-muted'}`} />
          </div>
        </div>

        <div className="grid gap-6 lg:grid-cols-2">
          {/* Upload Section */}
          <Card className="border-2">
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle className="flex items-center gap-2">
                  <Camera className="h-5 w-5 text-primary" />
                  Image Upload
                </CardTitle>
                <Button
                  variant="ghost"
                  size="sm"
                  className="h-8 text-foreground hover:text-primary transition-all duration-300 hover:scale-105 hover:bg-primary/10 font-medium"
                  onClick={() => router.push('/about')}
                >
                  <Info className="mr-2 h-4 w-4" />
                  About
                </Button>
              </div>
              <CardDescription>
                Select a clear image of your product
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex flex-col items-center justify-center">
                {previewUrl ? (
                  <div className="relative w-full aspect-square rounded-lg overflow-hidden border-2 border-border bg-muted">
                    <Image
                      src={previewUrl || "/placeholder.svg"}
                      alt="Selected product"
                      fill
                      className="object-cover"
                    />
                  </div>
                ) : (
                  <label className="flex flex-col items-center justify-center w-full aspect-square border-2 border-dashed border-border rounded-lg cursor-pointer hover:bg-accent/50 transition-colors">
                    <div className="flex flex-col items-center justify-center py-8">
                      <Upload className="h-12 w-12 text-muted-foreground mb-4" />
                      <p className="text-sm font-medium mb-1">Click to upload</p>
                      <p className="text-xs text-muted-foreground">PNG, JPG up to 10MB</p>
                    </div>
                    <input
                      type="file"
                      className="hidden"
                      accept="image/*"
                      onChange={handleImageSelect}
                    />
                  </label>
                )}
              </div>

              {selectedImage && currentStep === "upload" && (
                <div className="space-y-2">
                  <Button
                    onClick={handleUploadAndClassify}
                    disabled={isClassifying}
                    className="w-full"
                    size="lg"
                  >
                    {isClassifying ? (
                      <>
                        <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                        Classifying...
                      </>
                    ) : (
                      <>
                        <Upload className="mr-2 h-4 w-4" />
                        Upload & Classify
                      </>
                    )}
                  </Button>

                  <Button
                    onClick={handleRetry}
                    variant="outline"
                    className="w-full"
                  >
                    Choose Different Image
                  </Button>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Results & Forms Section */}
          <Card className={`border-2 ${classificationResult ? 'border-primary bg-primary/5' : ''}`}>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                {currentStep === "classify" && (
                  <>
                    <Edit className="h-5 w-5 text-primary" />
                    Confirm Classification
                  </>
                )}
                {currentStep === "metadata" && (
                  <>
                    <Edit className="h-5 w-5 text-primary" />
                    Enter Metadata
                  </>
                )}
                {currentStep === "review" && (
                  <>
                    <DollarSign className="h-5 w-5 text-primary" />
                    Price Prediction
                  </>
                )}
                {currentStep === "upload" && (
                  <>
                    <XCircle className="h-5 w-5 text-muted-foreground" />
                    Awaiting Upload
                  </>
                )}
              </CardTitle>
              <CardDescription>
                {currentStep === "classify" && "Review and confirm AI predictions"}
                {currentStep === "metadata" && "Provide additional information about the pet"}
                {currentStep === "review" && "Review predicted price and continue"}
                {currentStep === "upload" && "Results will appear here after classification"}
              </CardDescription>
            </CardHeader>
            <CardContent>
              {isClassifying ? (
                <div className="flex flex-col items-center justify-center py-12">
                  <Loader2 className="h-12 w-12 text-primary animate-spin mb-4" />
                  <p className="text-sm text-muted-foreground">Analyzing image with AI...</p>
                </div>
              ) : currentStep === "classify" && classificationResult ? (
                <div className="space-y-4">
                  {/* Product Type */}
                  <div className="space-y-2">
                    <Label htmlFor="product-type">Product Type</Label>
                    <Select value={editedType} onValueChange={setEditedType}>
                      <SelectTrigger id="product-type">
                        <SelectValue placeholder="Select type" />
                      </SelectTrigger>
                      <SelectContent>
                        {productTypes.map((type) => (
                          <SelectItem key={type.type_id} value={type.name}>
                            {type.name}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                    <p className="text-xs text-muted-foreground">
                      AI predicted: {classificationResult.productType}
                    </p>
                  </div>

                  {/* Product Name */}
                  <div className="space-y-2">
                    <Label htmlFor="product-name">Breed Name</Label>
                    <Input
                      id="product-name"
                      value={editedName}
                      onChange={(e) => setEditedName(e.target.value)}
                      placeholder="Enter breed name"
                    />
                    <p className="text-xs text-muted-foreground">
                      AI predicted: {classificationResult.productName}
                    </p>
                  </div>

                  <div className="flex flex-col gap-2 pt-4">
                    <Button
                      onClick={handleConfirmClassification}
                      size="lg"
                      className="w-full"
                    >
                      Continue to Metadata
                    </Button>

                    <Button
                      onClick={handleRetry}
                      variant="outline"
                      className="w-full"
                    >
                      Retry Upload
                    </Button>
                  </div>
                </div>
              ) : currentStep === "metadata" ? (
                <div className="space-y-4">
                  <div className="space-y-2">
                    <Label htmlFor="age">Age (months)</Label>
                    <Input
                      id="age"
                      type="number"
                      min="1"
                      max="120"
                      value={ageMonths}
                      onChange={(e) => setAgeMonths(e.target.value)}
                      placeholder="e.g., 6"
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="weight">Weight (kg)</Label>
                    <Input
                      id="weight"
                      type="number"
                      step="0.1"
                      min="0.1"
                      max="200"
                      value={weightKg}
                      onChange={(e) => setWeightKg(e.target.value)}
                      placeholder="e.g., 10.5"
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="health">Health Status</Label>
                    <Select value={healthStatus} onValueChange={setHealthStatus}>
                      <SelectTrigger id="health">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="0">Normal</SelectItem>
                        <SelectItem value="1">Good</SelectItem>
                        <SelectItem value="2">Excellent</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="flex items-center space-x-2">
                    <input
                      type="checkbox"
                      id="vaccinated"
                      checked={vaccinated}
                      onChange={(e) => setVaccinated(e.target.checked)}
                      className="h-4 w-4 rounded border-gray-300"
                    />
                    <Label htmlFor="vaccinated" className="cursor-pointer">
                      Vaccinated
                    </Label>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="country">Country of Origin</Label>
                    <Select value={country} onValueChange={setCountry}>
                      <SelectTrigger id="country">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="USA">USA</SelectItem>
                        <SelectItem value="Canada">Canada</SelectItem>
                        <SelectItem value="England">England</SelectItem>
                        <SelectItem value="Scotland">Scotland</SelectItem>
                        <SelectItem value="France">France</SelectItem>
                        <SelectItem value="Germany">Germany</SelectItem>
                        <SelectItem value="Iran">Iran</SelectItem>
                        <SelectItem value="Thailand">Thailand</SelectItem>
                        <SelectItem value="Russia">Russia</SelectItem>
                        <SelectItem value="Afghanistan">Afghanistan</SelectItem>
                        <SelectItem value="Ethiopia">Ethiopia</SelectItem>
                        <SelectItem value="Africa">Africa</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="flex flex-col gap-2 pt-4">
                    <Button
                      onClick={handlePredictPrice}
                      disabled={isPredictingPrice}
                      size="lg"
                      className="w-full"
                    >
                      {isPredictingPrice ? (
                        <>
                          <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                          Predicting Price...
                        </>
                      ) : (
                        <>
                          <DollarSign className="mr-2 h-4 w-4" />
                          Predict Price
                        </>
                      )}
                    </Button>

                    <Button
                      onClick={handleBack}
                      variant="outline"
                      className="w-full"
                    >
                      Back
                    </Button>
                  </div>
                </div>
              ) : currentStep === "review" && predictedPrice !== null ? (
                <div className="space-y-4">
                  <div className="bg-primary/10 rounded-lg p-6 text-center">
                    <p className="text-sm text-muted-foreground mb-2">Predicted Price</p>
                    <p className="text-4xl font-bold text-primary">${predictedPrice.toFixed(2)}</p>
                  </div>

                  <div className="text-sm space-y-1 text-muted-foreground">
                    <p>Type: {editedType}</p>
                    <p>Breed: {editedName}</p>
                    <p>Age: {ageMonths} months</p>
                    <p>Weight: {weightKg} kg</p>
                    <p>Health: {["Normal", "Good", "Excellent"][parseInt(healthStatus)]}</p>
                    <p>Vaccinated: {vaccinated ? "Yes" : "No"}</p>
                  </div>

                  <div className="flex flex-col gap-2 pt-4">
                    <Button
                      onClick={handleContinue}
                      size="lg"
                      className="w-full"
                    >
                      Continue to Add Product
                    </Button>

                    <Button
                      onClick={handleBack}
                      variant="outline"
                      className="w-full"
                    >
                      Edit Metadata
                    </Button>

                    <Button
                      onClick={handleRetry}
                      variant="ghost"
                      className="w-full"
                    >
                      Start Over
                    </Button>
                  </div>
                </div>
              ) : (
                <div className="flex flex-col items-center justify-center py-12 text-center">
                  <div className="h-16 w-16 rounded-full bg-muted flex items-center justify-center mb-4">
                    <Upload className="h-8 w-8 text-muted-foreground" />
                  </div>
                  <p className="text-sm text-muted-foreground">
                    Upload an image to see classification results
                  </p>
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </AuthGuard>
  )
}
