import { useLocation, useNavigate } from 'react-router-dom';
import Navbar from '@/components/Navbar';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { ArrowLeft, TrendingUp, TrendingDown } from 'lucide-react';

const CreditScoreResult = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { prediction, applicant } = location.state || {};

  if (!prediction && !applicant) {
    return (
      <div className="min-h-screen bg-background">
        <Navbar />
        <main className="container mx-auto px-4 py-8">
          <div className="text-center">
            <p className="text-muted-foreground">No data available</p>
            <Button onClick={() => navigate('/dashboard')} className="mt-4">
              Back to Dashboard
            </Button>
          </div>
        </main>
      </div>
    );
  }

  const score = prediction?.score || applicant?.credit_score;
  const riskTier = prediction?.risk_tier || applicant?.risk_tier;
  const featureImportances = prediction?.feature_importances || [];
  const confidence = prediction?.confidence;

  const getRiskColor = (tier?: string) => {
    switch (tier) {
      case 'low':
        return 'text-success';
      case 'medium':
        return 'text-warning';
      case 'high':
      case 'very_high':
        return 'text-destructive';
      default:
        return 'text-muted-foreground';
    }
  };

  const getRiskBadgeVariant = (tier?: string): any => {
    switch (tier) {
      case 'low':
        return 'default';
      case 'medium':
        return 'secondary';
      case 'high':
      case 'very_high':
        return 'destructive';
      default:
        return 'outline';
    }
  };

  const getScoreProgress = (score: number) => {
    return ((score - 300) / (850 - 300)) * 100;
  };

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      
      <main className="container mx-auto px-4 py-8">
        <Button
          variant="ghost"
          onClick={() => navigate('/dashboard')}
          className="mb-4"
        >
          <ArrowLeft className="mr-2 h-4 w-4" />
          Back to Dashboard
        </Button>

        <div className="grid gap-6 md:grid-cols-2">
          {/* Score Card */}
          <Card>
            <CardHeader>
              <CardTitle>Credit Score</CardTitle>
              <CardDescription>
                {applicant?.name || 'Applicant'}'s creditworthiness assessment
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-center">
                <div className={`mb-4 text-6xl font-bold ${getRiskColor(riskTier)}`}>
                  {score || 'N/A'}
                </div>
                <Badge variant={getRiskBadgeVariant(riskTier)} className="mb-4 text-lg">
                  {riskTier?.replace('_', ' ').toUpperCase() || 'NOT SCORED'}
                </Badge>
                {score && (
                  <>
                    <Progress value={getScoreProgress(score)} className="mb-2" />
                    <div className="flex justify-between text-sm text-muted-foreground">
                      <span>300</span>
                      <span>850</span>
                    </div>
                  </>
                )}
                {confidence && (
                  <div className="mt-4 text-sm text-muted-foreground">
                    Confidence: {(confidence * 100).toFixed(0)}%
                  </div>
                )}
              </div>
            </CardContent>
          </Card>

          {/* Risk Interpretation */}
          <Card>
            <CardHeader>
              <CardTitle>Risk Assessment</CardTitle>
              <CardDescription>What this score means</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {riskTier === 'low' && (
                  <div className="rounded-lg bg-success/10 p-4">
                    <div className="flex items-start gap-2">
                      <TrendingUp className="mt-0.5 h-5 w-5 text-success" />
                      <div>
                        <h4 className="font-semibold text-success">Excellent Credit</h4>
                        <p className="text-sm text-muted-foreground">
                          This applicant shows strong financial health and low risk. Ideal for lending.
                        </p>
                      </div>
                    </div>
                  </div>
                )}
                {riskTier === 'medium' && (
                  <div className="rounded-lg bg-warning/10 p-4">
                    <div className="flex items-start gap-2">
                      <TrendingUp className="mt-0.5 h-5 w-5 text-warning" />
                      <div>
                        <h4 className="font-semibold text-warning">Good Credit</h4>
                        <p className="text-sm text-muted-foreground">
                          Moderate risk profile. Consider additional verification before lending.
                        </p>
                      </div>
                    </div>
                  </div>
                )}
                {(riskTier === 'high' || riskTier === 'very_high') && (
                  <div className="rounded-lg bg-destructive/10 p-4">
                    <div className="flex items-start gap-2">
                      <TrendingDown className="mt-0.5 h-5 w-5 text-destructive" />
                      <div>
                        <h4 className="font-semibold text-destructive">High Risk</h4>
                        <p className="text-sm text-muted-foreground">
                          Elevated risk factors detected. Proceed with caution or require collateral.
                        </p>
                      </div>
                    </div>
                  </div>
                )}

                <div className="space-y-2 rounded-lg border border-border p-4">
                  <h4 className="font-semibold">Score Range Guide</h4>
                  <div className="space-y-1 text-sm">
                    <div className="flex justify-between">
                      <span>750-850:</span>
                      <span className="text-success">Excellent</span>
                    </div>
                    <div className="flex justify-between">
                      <span>650-749:</span>
                      <span className="text-warning">Good</span>
                    </div>
                    <div className="flex justify-between">
                      <span>550-649:</span>
                      <span className="text-destructive">Fair</span>
                    </div>
                    <div className="flex justify-between">
                      <span>300-549:</span>
                      <span className="text-destructive">Poor</span>
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Feature Importances */}
          {featureImportances.length > 0 && (
            <Card className="md:col-span-2">
              <CardHeader>
                <CardTitle>Contributing Factors</CardTitle>
                <CardDescription>Key signals that influenced the credit score</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {featureImportances.map((fi: any, index: number) => (
                    <div key={index} className="space-y-2">
                      <div className="flex items-center justify-between">
                        <span className="font-medium">{fi.feature}</span>
                        <span className="text-sm text-muted-foreground">
                          {(fi.importance * 100).toFixed(0)}% impact
                        </span>
                      </div>
                      <Progress value={fi.importance * 100} />
                      <div className="text-sm text-muted-foreground">
                        Value: {typeof fi.value === 'number' ? fi.value.toFixed(2) : fi.value}
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}
        </div>
      </main>
    </div>
  );
};

export default CreditScoreResult;
