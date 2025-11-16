import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import Navbar from '@/components/Navbar';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { ArrowLeft } from 'lucide-react';
import api from '@/services/api';
import { toast } from 'sonner';

const basicInfoSchema = z.object({
  name: z.string().min(2, 'Name must be at least 2 characters'),
  email: z.string().email('Invalid email address'),
  phone: z.string().optional(),
});

const financialSchema = z.object({
  monthly_income: z.number().positive('Income must be positive'),
  monthly_expenses: z.number().nonnegative('Expenses cannot be negative'),
  savings: z.number().nonnegative('Savings cannot be negative'),
  existing_loans: z.number().nonnegative('Loans cannot be negative'),
  payment_history_score: z.number().min(0).max(100),
});

const socialSchema = z.object({
  social_connections: z.number().int().nonnegative(),
  community_engagement_score: z.number().min(0).max(100),
  references_count: z.number().int().nonnegative(),
  online_reputation_score: z.number().min(0).max(100),
});

const gigSchema = z.object({
  platforms: z.string(), // Will be split into array
  total_gigs_completed: z.number().int().nonnegative(),
  average_rating: z.number().min(0).max(5),
  active_months: z.number().int().nonnegative(),
  income_consistency_score: z.number().min(0).max(100),
});

type BasicInfo = z.infer<typeof basicInfoSchema>;
type FinancialData = z.infer<typeof financialSchema>;
type SocialData = z.infer<typeof socialSchema>;
type GigData = z.infer<typeof gigSchema>;

const ApplicantForm = () => {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('basic');
  const [submitting, setSubmitting] = useState(false);

  const basicForm = useForm<BasicInfo>({
    resolver: zodResolver(basicInfoSchema),
  });

  const financialForm = useForm<FinancialData>({
    resolver: zodResolver(financialSchema),
    defaultValues: {
      existing_loans: 0,
      payment_history_score: 50,
    },
  });

  const socialForm = useForm<SocialData>({
    resolver: zodResolver(socialSchema),
    defaultValues: {
      social_connections: 0,
      community_engagement_score: 50,
      references_count: 0,
      online_reputation_score: 50,
    },
  });

  const gigForm = useForm<GigData>({
    resolver: zodResolver(gigSchema),
    defaultValues: {
      platforms: '',
      total_gigs_completed: 0,
      average_rating: 0,
      active_months: 0,
      income_consistency_score: 50,
    },
  });

  const handleSubmit = async () => {
    // Validate all forms
    const basicValid = await basicForm.trigger();
    const financialValid = await financialForm.trigger();
    const socialValid = await socialForm.trigger();
    const gigValid = await gigForm.trigger();

    if (!basicValid || !financialValid || !socialValid || !gigValid) {
      toast.error('Please fill in all required fields');
      return;
    }

    setSubmitting(true);

    try {
      const basicData = basicForm.getValues();
      const financialData = financialForm.getValues();
      const socialData = socialForm.getValues();
      const gigData = gigForm.getValues();

      const payload = {
        name: basicData.name,
        email: basicData.email,
        phone: basicData.phone,
        financial_data: financialData,
        social_data: socialData,
        gig_data: {
          ...gigData,
          platforms: gigData.platforms.split(',').map((p) => p.trim()).filter(Boolean),
        },
      };

      await api.post('/ingest/applicant', payload);
      toast.success('Applicant added successfully!');
      navigate('/dashboard');
    } catch (error: any) {
      console.error('Failed to add applicant:', error);
      toast.error(error.response?.data?.detail || 'Failed to add applicant');
    } finally {
      setSubmitting(false);
    }
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

        <Card>
          <CardHeader>
            <CardTitle>Add New Applicant</CardTitle>
            <CardDescription>
              Collect comprehensive data for credit scoring
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Tabs value={activeTab} onValueChange={setActiveTab}>
              <TabsList className="grid w-full grid-cols-4">
                <TabsTrigger value="basic">Basic</TabsTrigger>
                <TabsTrigger value="financial">Financial</TabsTrigger>
                <TabsTrigger value="social">Social</TabsTrigger>
                <TabsTrigger value="gig">Gig Economy</TabsTrigger>
              </TabsList>

              <TabsContent value="basic" className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="name">Full Name *</Label>
                  <Input
                    id="name"
                    {...basicForm.register('name')}
                    placeholder="John Doe"
                  />
                  {basicForm.formState.errors.name && (
                    <p className="text-sm text-destructive">
                      {basicForm.formState.errors.name.message}
                    </p>
                  )}
                </div>

                <div className="space-y-2">
                  <Label htmlFor="email">Email *</Label>
                  <Input
                    id="email"
                    type="email"
                    {...basicForm.register('email')}
                    placeholder="john@example.com"
                  />
                  {basicForm.formState.errors.email && (
                    <p className="text-sm text-destructive">
                      {basicForm.formState.errors.email.message}
                    </p>
                  )}
                </div>

                <div className="space-y-2">
                  <Label htmlFor="phone">Phone</Label>
                  <Input
                    id="phone"
                    {...basicForm.register('phone')}
                    placeholder="+91 1234567890"
                  />
                </div>
              </TabsContent>

              <TabsContent value="financial" className="space-y-4">
                <div className="grid gap-4 md:grid-cols-2">
                  <div className="space-y-2">
                    <Label htmlFor="monthly_income">Monthly Income (₹) *</Label>
                    <Input
                      id="monthly_income"
                      type="number"
                      {...financialForm.register('monthly_income', { valueAsNumber: true })}
                      placeholder="30000"
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="monthly_expenses">Monthly Expenses (₹) *</Label>
                    <Input
                      id="monthly_expenses"
                      type="number"
                      {...financialForm.register('monthly_expenses', { valueAsNumber: true })}
                      placeholder="20000"
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="savings">Savings (₹) *</Label>
                    <Input
                      id="savings"
                      type="number"
                      {...financialForm.register('savings', { valueAsNumber: true })}
                      placeholder="50000"
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="existing_loans">Existing Loans (₹)</Label>
                    <Input
                      id="existing_loans"
                      type="number"
                      {...financialForm.register('existing_loans', { valueAsNumber: true })}
                      placeholder="0"
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="payment_history_score">Payment History Score (0-100)</Label>
                    <Input
                      id="payment_history_score"
                      type="number"
                      {...financialForm.register('payment_history_score', { valueAsNumber: true })}
                      placeholder="75"
                    />
                  </div>
                </div>
              </TabsContent>

              <TabsContent value="social" className="space-y-4">
                <div className="grid gap-4 md:grid-cols-2">
                  <div className="space-y-2">
                    <Label htmlFor="social_connections">Social Connections</Label>
                    <Input
                      id="social_connections"
                      type="number"
                      {...socialForm.register('social_connections', { valueAsNumber: true })}
                      placeholder="200"
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="community_engagement_score">Community Engagement (0-100)</Label>
                    <Input
                      id="community_engagement_score"
                      type="number"
                      {...socialForm.register('community_engagement_score', { valueAsNumber: true })}
                      placeholder="60"
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="references_count">References Count</Label>
                    <Input
                      id="references_count"
                      type="number"
                      {...socialForm.register('references_count', { valueAsNumber: true })}
                      placeholder="3"
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="online_reputation_score">Online Reputation (0-100)</Label>
                    <Input
                      id="online_reputation_score"
                      type="number"
                      {...socialForm.register('online_reputation_score', { valueAsNumber: true })}
                      placeholder="70"
                    />
                  </div>
                </div>
              </TabsContent>

              <TabsContent value="gig" className="space-y-4">
                <div className="grid gap-4 md:grid-cols-2">
                  <div className="space-y-2 md:col-span-2">
                    <Label htmlFor="platforms">Platforms (comma-separated)</Label>
                    <Input
                      id="platforms"
                      {...gigForm.register('platforms')}
                      placeholder="Uber, Swiggy, Zomato"
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="total_gigs_completed">Total Gigs Completed</Label>
                    <Input
                      id="total_gigs_completed"
                      type="number"
                      {...gigForm.register('total_gigs_completed', { valueAsNumber: true })}
                      placeholder="150"
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="average_rating">Average Rating (0-5)</Label>
                    <Input
                      id="average_rating"
                      type="number"
                      step="0.1"
                      {...gigForm.register('average_rating', { valueAsNumber: true })}
                      placeholder="4.5"
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="active_months">Active Months</Label>
                    <Input
                      id="active_months"
                      type="number"
                      {...gigForm.register('active_months', { valueAsNumber: true })}
                      placeholder="12"
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="income_consistency_score">Income Consistency (0-100)</Label>
                    <Input
                      id="income_consistency_score"
                      type="number"
                      {...gigForm.register('income_consistency_score', { valueAsNumber: true })}
                      placeholder="75"
                    />
                  </div>
                </div>
              </TabsContent>
            </Tabs>

            <div className="mt-6 flex gap-2">
              <Button onClick={handleSubmit} disabled={submitting} className="flex-1">
                {submitting ? 'Saving...' : 'Save Applicant'}
              </Button>
              <Button variant="outline" onClick={() => navigate('/dashboard')}>
                Cancel
              </Button>
            </div>
          </CardContent>
        </Card>
      </main>
    </div>
  );
};

export default ApplicantForm;
