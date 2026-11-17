/**
 * The Practice - Standalone Interactive Engine
 */

document.addEventListener("DOMContentLoaded", () => {
  // --- 1. FAQ Accordion Engine ---
  const FAQ_DATA = {
    "How do I know if therapy is right for me?": "There’s no wrong reason to reach out. If something is weighing on you, affecting your sleep, work or relationships — or you simply want space to think — therapy can help. A free consultation is a no-pressure way to find out.",
    "How do I get started?": "Just request a free 15-minute consultation through our website. We’ll reach out to learn a little about what you’re looking for and match you with the right therapist on our team.",
    "What happens in the free consultation?": "It’s a brief, informal phone or video call. You can share what’s bringing you to therapy, ask questions about our approach, and see if we feel like the right fit before scheduling a full session.",
    "How do you match me with a therapist?": "We consider what you’re hoping to work on, your schedule, and any personal preferences you have (such as approach, style, or background) to pair you with someone best suited to your needs.",
    "Can I switch therapists?": "Yes, absolutely. The therapeutic relationship is deeply personal. If you feel like your match isn’t quite right at any point, let us know and we’ll transition you seamlessly to another therapist.",
    "Do I need a referral?": "No referral is needed to begin working with us. You can reach out directly whenever you’re ready.",
    "How long is each session?": "Standard individual sessions are 50 minutes. Couples and family sessions are typically 60 to 75 minutes depending on your therapist and treatment plan.",
    "How often will we meet?": "Most clients start meeting once a week. Meeting weekly creates momentum and consistency. Over time, as you make progress, you and your therapist may decide to taper to biweekly sessions.",
    "What happens in the first session?": "Your first full session is an intake where we take time to understand your history, what’s going on right now, and what you hope to get out of therapy. There’s no pressure to share more than you’re ready to.",
    "Do you offer online sessions?": "Yes, we offer secure, confidential video therapy for clients residing anywhere in the states we are licensed in. Online therapy is just as effective as in-person care.",
    "Do you work with couples and families?": "Yes. Several clinicians on our team specialize in relationship therapy, communication, conflict resolution, and supporting teens and their families.",
    "How long does therapy usually take?": "It depends on your unique goals and needs. Some clients find clarity and resolution in 8–12 sessions, while others benefit from ongoing, open-ended support for deeper personal growth.",
    "How much does therapy cost?": "Fees vary by service and therapist. We’ll share current rates during your free consultation, before you commit to anything.",
    "How much does therapy cost? Do you take insurance?": "Fees vary by clinician and session type. We’ll walk you through costs and insurance options during your free consultation, before you commit to anything.",
    "Do you take insurance?": "Coverage varies by plan. We can talk you through your options during your consultation and provide receipts you may be able to submit to your insurer.",
    "Do you offer reduced fees?": "Ask us during your consultation — we’ll always try to help you find an option that works for you.",
    "What is your cancellation policy?": "We ask for at least 24 hours’ notice to cancel or reschedule, so we can offer the time to someone else.",
    "How do I pay?": "You can pay securely by card after each session, and we’ll email you a receipt.",
    "Is what I share kept confidential?": "Yes. Confidentiality is a legal and ethical cornerstone of therapy. Everything discussed remains strictly private between you and your therapist.",
    "Are there limits to confidentiality?": "The only exceptions are legally mandated situations involving imminent danger to yourself or others, or suspected abuse of a child, elder, or vulnerable adult.",
    "How is my information stored?": "We use HIPAA-compliant electronic health record systems that use end-to-end encryption to store notes, scheduling, and billing details safely.",
    "Is online therapy secure?": "Yes. We use encrypted, HIPAA-compliant telehealth software to ensure your video and audio data remain completely confidential.",
    "What if I’m in crisis?": "We are an outpatient practice and not an emergency service. If you are experiencing a mental health emergency, please call or text 988 or go to the nearest emergency room immediately."
  };

  // Find all question cards (target the inner interactive card uniquely)
  const questionElements = document.querySelectorAll('.framer-0BDWv');
  questionElements.forEach((el) => {
    // Find the question text
    const heading = el.querySelector("h5, [data-framer-name='Question']");
    if (!heading) return;
    const qText = heading.textContent.trim();
    const answer = FAQ_DATA[qText];
    if (!answer) return;

    // Make interactive cursor
    el.style.cursor = "pointer";

    // Create answer container
    let answerBox = el.querySelector(".faq-answer-box");
    if (!answerBox) {
      answerBox = document.createElement("div");
      answerBox.className = "faq-answer-box";
      answerBox.style.display = "none";
      answerBox.textContent = answer;
      el.appendChild(answerBox);
    }

    const iconSvg = el.querySelector("[data-framer-name='Icon'] svg");
    if (iconSvg) {
      iconSvg.classList.add("faq-icon-rotator");
    }

    el.addEventListener("click", (e) => {
      e.stopPropagation();
      const isOpen = el.classList.contains("faq-open");
      if (isOpen) {
        el.classList.remove("faq-open");
        answerBox.style.display = "none";
      } else {
        el.classList.add("faq-open");
        answerBox.style.display = "block";
      }
    });
  });

  // --- 2. Mobile Navigation Toggle ---
  const menuButtons = document.querySelectorAll('[data-framer-name="Menu Button"], button[aria-label="Toggle menu"]');
  menuButtons.forEach((btn) => {
    btn.addEventListener("click", (e) => {
      e.preventDefault();
      e.stopPropagation();
      const nav = btn.closest("nav");
      if (nav) {
        nav.classList.toggle("mobile-nav-open");
      }
    });
  });
});
