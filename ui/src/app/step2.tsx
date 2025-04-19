"use client";

import { validateSubscription } from "@/api/subscription";
import { Button } from "@/components/button";
import { Field, Fieldset, Label } from "@/components/fieldset";
import { Strong, Text } from "@/components/text";
import { Textarea } from "@/components/textarea";
import { CheckCircleIcon } from "@heroicons/react/20/solid";

export default function Step2({
  setCurrentStep,
  subscriptionToken,
}: {
  setCurrentStep: (step: number) => void;
  subscriptionToken: string;
}) {
  const handleValidation = () => {
    if (!subscriptionToken) return;

    validateSubscription(subscriptionToken)
      .then(() => {
        setCurrentStep(3); // Proceed to the next step
      })
      .catch((error) => {
        // Handle any errors that occur during validation
        console.error("Validation error:", error);
      });
  };

  return (
    <Fieldset className="w-96 space-y-6">
      <Text>
        <Strong>OK, let&apos;s be honest</Strong> — the application is still
        under development, and the backend isn&apos;t fully ready yet.
      </Text>
      <Text>
        Currently, the API is generating a token that&apos;s meant to be
        embedded in an email body. This token contains all the information about
        your subscription <Strong>encoded</Strong> and
        <Strong> encrypted</Strong> and will eventually be used to validate and
        initiate the subscription process. The token expires after 5 minutes.
      </Text>
      <Text>
        However,
        <Strong>
          {" "}
          the email service hasn&apos;t been implemented yet, so you won&apos;t
          be receiving any emails for now.
        </Strong>
      </Text>
      <Field>
        <Label>This is the token given by the API.</Label>
        <Textarea
          readOnly
          name="validationToken"
          defaultValue={subscriptionToken}
          rows={6}
        />
      </Field>
      <Text>
        So let&apos;s imagine this is the email you would receive. It should
        have a button like the own below.
      </Text>
      <Button
        color="indigo"
        onClick={handleValidation}
        className="hover:cursor-pointer w-96 mt-2"
      >
        <CheckCircleIcon />
        Validate Subscription
      </Button>
    </Fieldset>
  );
}
