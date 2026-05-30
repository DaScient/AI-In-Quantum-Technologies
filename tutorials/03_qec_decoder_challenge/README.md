# Tutorial 3 — Quantum Error Correction Decoder Challenge

**Chapter:** 8 (Quantum Error Correction & Mitigation)

Build and benchmark your own decoder. This path generates a labelled corpus of
bit-flip repetition-code errors and syndromes, evaluates the built-in
minimum-weight decoder, and invites you to beat it with a learned model. A simple
logical-error-rate metric provides the leaderboard score.

## What you will learn

- How syndromes relate to errors in a stabiliser code (Chapter 8).
- How to score a decoder by its logical error rate.
- Where machine learning can improve on minimum-weight matching.

## Run it

```bash
python tutorials/03_qec_decoder_challenge/walkthrough.py
```

The script samples a syndrome dataset, decodes each syndrome with
`decode_repetition_code`, and reports the logical error rate. To enter the
challenge, replace the decoder with your own (e.g. a neural network trained on the
`errors`/`syndromes` arrays) and compare the score.
