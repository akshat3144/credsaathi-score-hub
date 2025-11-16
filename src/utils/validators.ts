import { z } from 'zod';

export const applicantSchema = z.object({
  name: z.string().min(2, "Name must be at least 2 characters"),
  email: z.string().email("Invalid email address"),
  phone: z.string().optional(),
});

export const financialSchema = z.object({
  monthly_income: z.number().positive("Income must be positive"),
  monthly_expenses: z.number().nonnegative("Expenses cannot be negative"),
  savings: z.number().nonnegative("Savings cannot be negative"),
  existing_loans: z.number().nonnegative("Loans cannot be negative").default(0),
  payment_history_score: z.number().min(0).max(100).default(0),
});

export const socialSchema = z.object({
  social_connections: z.number().int().nonnegative().default(0),
  community_engagement_score: z.number().min(0).max(100).default(0),
  references_count: z.number().int().nonnegative().default(0),
  online_reputation_score: z.number().min(0).max(100).default(0),
});

export const gigSchema = z.object({
  platforms: z.array(z.string()).default([]),
  total_gigs_completed: z.number().int().nonnegative().default(0),
  average_rating: z.number().min(0).max(5).default(0),
  active_months: z.number().int().nonnegative().default(0),
  income_consistency_score: z.number().min(0).max(100).default(0),
});

export type ApplicantFormData = z.infer<typeof applicantSchema>;
export type FinancialData = z.infer<typeof financialSchema>;
export type SocialData = z.infer<typeof socialSchema>;
export type GigData = z.infer<typeof gigSchema>;
