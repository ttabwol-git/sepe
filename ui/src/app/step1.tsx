"use client";

import { fetchPostals } from "@/api/postal";
import { queueSubscription } from "@/api/subscription";
import { Button } from "@/components/button";
import { Combobox, ComboboxLabel, ComboboxOption } from "@/components/combobox";
import { Description, Field, Fieldset, Label } from "@/components/fieldset";
import { Input } from "@/components/input";
import { Strong, Text } from "@/components/text";
import { PaperAirplaneIcon } from "@heroicons/react/20/solid";
import clsx from "clsx";
import { useCallback, useEffect, useState } from "react";

export default function Step1({
  setCurrentStep,
  setSubscriptionToken,
}: {
  setCurrentStep: (step: number) => void;
  setSubscriptionToken: (token: string) => void;
}) {
  interface Postal { code: string };
  interface SubscriptionResponse { validation_token: string };
  const [postals, setPostals] = useState<Postal[]>([]);
  const [selectedPostal, setSelectedPostal] = useState<Postal | null>(null);
  const [selectedEmail, setSelectedEmail] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      if (postals.length > 0) return; // Avoid fetching if already fetched
      try {
        const data: Array<Postal> = await fetchPostals();
        setPostals(data);
        setSelectedPostal(null); // Let the user choose manually
      } catch (err) {
        console.error("Error fetching postals:", err);
      }
    };
    fetchData();
  }, [postals.length]);

  const handlePostalChange = (postal: Postal) => setSelectedPostal(postal);
  const handleEmailChange = (e: React.ChangeEvent<HTMLInputElement>) =>
    setSelectedEmail(e.target.value);

  const handleSubmit = useCallback(async () => {
    if (!selectedPostal || !selectedEmail) return;

    setIsSubmitting(true);

    try {
      const response: SubscriptionResponse = await queueSubscription(
        selectedPostal.code,
        selectedEmail
      );

      if (response?.validation_token) {
        setSubscriptionToken(response.validation_token);
        setCurrentStep(2); // Proceed to the next step
      }
    } catch (err) {
      console.error("Subscription error:", err);
    } finally {
      setIsSubmitting(false);
    }
  }, [selectedPostal, selectedEmail, setCurrentStep, setSubscriptionToken]);

  const isDisabled = !selectedEmail || !selectedPostal || isSubmitting;

  return (
    <Fieldset className="w-96 space-y-10">
      <Text>
        Lost your job? Need your unemployment subsidy as soon as possible?
        Struggling to find an available SEPE office? Don&apos;t worry —
        <Strong>we&apos;ve got you covered</Strong>.
      </Text>
      <Text>
        By submitting your email address and postal code, you’ll be placed in
        the subscription queue.{" "}
        <Strong>This subscription must be validated</Strong> before the system
        can start checking availability.
      </Text>
      <Text>
        I suggest you keep the backend console open to see the logs on real time
        :)
      </Text>
      <Field>
        <Label>Postal Code</Label>
        <Description>Select the postal code of your area.</Description>
        <Combobox
          name="postal-code"
          options={postals}
          displayValue={(postal) => postal?.code}
          placeholder="..."
          className="max-h-96"
          onChange={handlePostalChange}
        >
          {(postal) => (
            <ComboboxOption value={postal}>
              <ComboboxLabel>{postal.code}</ComboboxLabel>
            </ComboboxOption>
          )}
        </Combobox>
      </Field>

      <Field className="pb-8">
        <Label>Email Address</Label>
        <Description>
          Enter the email address where you want to receive alerts.
        </Description>
        <Input
          name="email"
          placeholder="name@domain.com"
          type="email"
          onChange={handleEmailChange}
        />
      </Field>
      <Button
        disabled={isDisabled}
        className={clsx("w-96", {
          "cursor-not-allowed opacity-50": isDisabled,
          "cursor-pointer": !isDisabled,
        })}
        color="indigo"
        onClick={handleSubmit}
      >
        <PaperAirplaneIcon />
        {isSubmitting ? "Submitting..." : "Request"}
      </Button>
    </Fieldset>
  );
}
