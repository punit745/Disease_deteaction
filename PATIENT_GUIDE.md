# Patient User Guide - Disease Detection System

## Welcome to the Disease Detection System

This guide will help you use the disease detection system effectively as a patient.

## What is This System?

The Eye Tracking Disease Detection System analyzes your eye movement patterns to screen for early signs of neurological and developmental disorders, including:

- **Parkinson's Disease**: Movement disorder affecting the nervous system
- **Alzheimer's Disease**: Progressive memory and cognitive decline
- **Autism Spectrum Disorder (ASD)**: Developmental disorder affecting communication and behavior
- **ADHD**: Attention deficit hyperactivity disorder

**Important**: This is a screening tool only. Results should be discussed with qualified healthcare professionals for proper diagnosis.

## Getting Started

### Step 1: Create an Account

1. Visit the registration page or use the CLI tool
2. Provide your information:
   - Email address (for login)
   - Secure password
   - First and last name
   - Date of birth (optional but recommended)

### Step 2: Collect Eye Tracking Data

You'll need eye tracking data for analysis. This can be obtained through:

1. **Eye tracking devices**: Specialized hardware that tracks eye movements
2. **Research facilities**: Many universities have eye tracking equipment
3. **Healthcare providers**: Some clinics offer eye tracking assessments
4. **Sample data**: For testing, you can use generated sample data

### Step 3: Submit Data for Analysis

#### Using the Web API

```bash
# Login to get your token
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "your@email.com", "password": "your_password"}'

# Submit eye tracking data
curl -X POST http://localhost:5000/api/analyze \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d @your_data.json
```

#### Using the Command-Line Tool

```bash
# Analyze sample data (for testing)
python cli.py analyze --sample

# Analyze your own data file
python cli.py analyze --file your_data.json
```

### Step 4: Review Your Results

After analysis, you can:

1. **View all test results**:
   ```bash
   python cli.py results
   ```

2. **Get detailed analysis**:
   ```bash
   python cli.py result TEST_ID
   ```

3. **Generate comprehensive report**:
   ```bash
   python cli.py report TEST_ID
   ```

4. **View your statistics and trends**:
   ```bash
   python cli.py stats
   ```

## Understanding Your Results

### Risk Scores

Each disease is assigned a risk score from 0.0 to 1.0:

- **0.0 - 0.29**: Low Risk - Patterns are within normal range
- **0.30 - 0.59**: Moderate Risk - Some concerning patterns detected
- **0.60 - 1.0**: High Risk - Multiple indicators present

### Risk Levels

Results are categorized into three levels:

#### Low Risk
- Eye movement patterns appear normal
- No significant indicators detected
- Continue regular health monitoring
- No immediate action needed

#### Moderate Risk
- Some atypical patterns detected
- May warrant further observation
- Consider discussing with healthcare provider
- Schedule follow-up tests if recommended

#### High Risk
- Multiple concerning indicators present
- Professional evaluation recommended
- Consult with neurologist or specialist
- Additional diagnostic tests may be needed

### Disease-Specific Indicators

The system looks for specific patterns for each disorder:

#### Parkinson's Disease Indicators
- Reduced saccade (rapid eye movement) velocity
- Hypometric saccades (undershooting targets)
- Prolonged fixations
- Reduced saccade rate

#### Alzheimer's Disease Indicators
- Significantly prolonged fixations
- Reduced visual exploration
- High saccade variability
- Reduced saccade rate

#### Autism Spectrum Disorder Indicators
- High fixation duration variability
- Atypical spatial attention patterns
- Elevated saccade velocity
- Elevated saccade rate

#### ADHD Indicators
- Shortened fixations
- Elevated saccade rate
- High spatial dispersion
- High movement variability

## Data Privacy and Security

### Your Data is Protected

- **Encryption**: All data is encrypted in transit and at rest
- **Authentication**: Secure login with JWT tokens
- **Access Control**: Only you can access your test results
- **HIPAA Considerations**: System designed with healthcare data privacy in mind

### Your Rights

- You own your data
- You can request data deletion
- You can export your results
- You control who sees your information

## Preparing for Your Test

### Best Practices

1. **Rest well**: Get adequate sleep before the test
2. **Avoid substances**: No alcohol or drugs that may affect vision
3. **Wear glasses/contacts**: If you normally use them
4. **Relax**: Stress can affect eye movements
5. **Follow instructions**: Complete the task as directed

### What to Avoid

- Testing when tired or drowsy
- Testing immediately after eye strain
- Testing while under the influence
- Rushing through the test
- Looking away from the screen during testing

## Interpreting Recommendations

### Common Recommendations

#### "Consider neurological consultation"
- Schedule appointment with neurologist
- Bring your test results
- Discuss symptoms and concerns
- Ask about additional diagnostic tests

#### "Monitor motor symptoms"
- Keep a symptom diary
- Note any tremors or stiffness
- Track changes over time
- Report changes to doctor

#### "Consider cognitive assessment"
- Schedule neuropsychological evaluation
- Memory and thinking tests
- Discuss concerns with healthcare provider

#### "Consider attention assessment"
- Evaluation by psychologist or psychiatrist
- ADHD-specific testing
- Discuss impact on daily life

### When to Seek Immediate Medical Attention

Contact a healthcare provider promptly if you experience:

- Sudden changes in vision
- Rapid onset of symptoms
- Severe tremors or movement problems
- Significant memory loss
- Difficulty with daily activities

## Tracking Your Progress

### Test History

The system maintains a complete history of your tests, allowing you to:

- Compare results over time
- Track risk score trends
- Identify changes in patterns
- Share comprehensive data with doctors

### Understanding Trends

- **Stable scores**: Consistent patterns over time
- **Improving scores**: Risk scores decreasing
- **Worsening scores**: Risk scores increasing - consult healthcare provider
- **Fluctuating scores**: May be normal variation or testing conditions

## Frequently Asked Questions

### Q: How accurate is this screening?

A: This is a screening tool, not a diagnostic tool. It can identify patterns that may warrant further investigation but cannot diagnose disorders. Always consult healthcare professionals for proper diagnosis.

### Q: How often should I test?

A: Frequency depends on your individual situation. Consult with your healthcare provider. Generally:
- Baseline test: Initial screening
- Follow-up: Every 6-12 months if moderate/high risk
- As needed: If symptoms change

### Q: What if I get a high-risk result?

A: Don't panic. High-risk means indicators are present, not that you definitely have the disorder. Schedule an appointment with a healthcare provider to discuss results and next steps.

### Q: Can I share results with my doctor?

A: Yes! You can generate detailed reports and export your data to share with healthcare providers. They can use this as supplementary information alongside other assessments.

### Q: Is my data secure?

A: Yes. The system uses industry-standard security practices including encryption, secure authentication, and access controls.

### Q: What if I can't obtain eye tracking data?

A: Eye tracking equipment is available at:
- University research labs
- Some healthcare facilities
- Vision clinics
- Specialized testing centers

Contact local universities or medical centers to inquire about availability.

## Getting Help

### Technical Support

- **GitHub Issues**: Report bugs or request features
- **Documentation**: See README.md and API_DOCUMENTATION.md
- **Deployment Help**: See DEPLOYMENT.md

### Medical Questions

- **Consult your doctor**: For medical advice
- **Neurologist**: For neurological concerns
- **Psychologist/Psychiatrist**: For cognitive/behavioral concerns

## Important Disclaimers

⚠️ **Medical Disclaimer**

This software is provided for screening and research purposes only. It is NOT intended for:
- Clinical diagnosis
- Medical decision-making
- Treatment planning
- Emergency medical situations

Always consult qualified healthcare professionals for:
- Medical advice
- Diagnosis confirmation
- Treatment recommendations
- Emergency care

The developers and providers of this system are not liable for any medical decisions made based on the results.

## Next Steps

1. ✅ Create your account
2. ✅ Obtain eye tracking data
3. ✅ Submit data for analysis
4. ✅ Review your results
5. ✅ Consult with healthcare provider if needed
6. ✅ Track your progress over time

## Additional Resources

### Learn More About Eye Tracking

- Research papers on eye tracking in neurological assessment
- Information about the diseases screened
- Understanding eye movement patterns
- Latest research in early detection

### Community and Support

- Join research studies
- Participate in clinical trials
- Connect with support groups
- Share feedback to improve the system

---

**Remember**: This is a tool to assist in early detection and screening. Professional medical evaluation is essential for proper diagnosis and treatment.

For the latest information and updates, visit the project repository at:
https://github.com/punit745/Disease_deteaction-
